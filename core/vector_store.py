"""
向量数据库核心模块
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class VectorStore:
    """向量数据库管理类"""
    
    def __init__(self):
        self.vector_db = None
        self.embeddings = None
        self.text_splitter = None
        self._initialize()
    
    def _initialize(self):
        """初始化向量数据库"""
        try:
            # 初始化嵌入模型
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                cache_folder=str(settings.CACHE_DIR)
            )
            
            # 初始化文本分割器
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            # 根据配置选择向量数据库类型
            if settings.VECTOR_DB_TYPE == "chroma":
                self._init_chroma()
            elif settings.VECTOR_DB_TYPE == "faiss":
                self._init_faiss()
            else:
                raise ValueError(f"不支持的向量数据库类型: {settings.VECTOR_DB_TYPE}")
                
            logger.info(f"向量数据库初始化成功: {settings.VECTOR_DB_TYPE}")
            
        except Exception as e:
            logger.error(f"向量数据库初始化失败: {e}")
            raise
    
    def _init_chroma(self):
        """初始化Chroma向量数据库"""
        persist_directory = str(settings.VECTOR_DB_DIR / "chroma")
        
        try:
            if os.path.exists(persist_directory) and os.listdir(persist_directory):
                # 尝试加载已存在的数据库
                try:
                    self.vector_db = Chroma(
                        persist_directory=persist_directory,
                        embedding_function=self.embeddings
                    )
                    logger.info("加载已存在的Chroma向量数据库")
                    return
                except Exception as e:
                    logger.warning(f"加载现有数据库失败，重新创建: {e}")
                    # 删除损坏的数据库
                    import shutil
                    shutil.rmtree(persist_directory)
            
            # 创建新的数据库
            self._create_new_chroma(persist_directory)
            
        except Exception as e:
            logger.error(f"Chroma初始化失败: {e}")
            # 尝试使用FAISS作为备用方案
            logger.info("尝试使用FAISS作为备用方案...")
            self._init_faiss_fallback()
    
    def _create_new_chroma(self, persist_directory: str):
        """创建新的Chroma数据库"""
        try:
            # 确保目录存在
            os.makedirs(persist_directory, exist_ok=True)
            
            # 创建新的Chroma数据库
            self.vector_db = Chroma(
                embedding_function=self.embeddings,
                persist_directory=persist_directory
            )
            logger.info("创建新的Chroma向量数据库")
            
        except Exception as e:
            logger.error(f"创建新Chroma数据库失败: {e}")
            raise
    
    def _init_faiss_fallback(self):
        """使用FAISS作为备用方案"""
        try:
            logger.info("切换到FAISS向量数据库")
            settings.VECTOR_DB_TYPE = "faiss"
            self._init_faiss()
        except Exception as e:
            logger.error(f"FAISS备用方案也失败: {e}")
            raise
    
    def _init_faiss(self):
        """初始化FAISS向量数据库"""
        faiss_index_path = settings.VECTOR_DB_DIR / "faiss"
        
        try:
            if faiss_index_path.exists():
                # 加载已存在的索引
                self.vector_db = FAISS.load_local(
                    str(faiss_index_path),
                    self.embeddings
                )
                logger.info("加载已存在的FAISS向量数据库")
            else:
                # 创建新的索引
                self.vector_db = FAISS.from_texts(
                    ["初始化文档"],
                    self.embeddings
                )
                logger.info("创建新的FAISS向量数据库")
                
        except Exception as e:
            logger.error(f"FAISS初始化失败: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """添加文档到向量数据库"""
        try:
            # 分割文档
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"文档分割完成，共{len(split_docs)}个片段")
            
            # 添加到向量数据库
            if isinstance(self.vector_db, Chroma):
                self.vector_db.add_documents(split_docs)
                # 新版本Chroma自动持久化，不需要手动调用persist()
                logger.info("文档已添加到Chroma数据库")
            elif isinstance(self.vector_db, FAISS):
                self.vector_db.add_documents(split_docs)
                # 保存FAISS索引
                faiss_index_path = settings.VECTOR_DB_DIR / "faiss"
                self.vector_db.save_local(str(faiss_index_path))
                logger.info("文档已添加到FAISS数据库")
            
            logger.info(f"成功添加{len(split_docs)}个文档片段到向量数据库")
            
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            raise
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> None:
        """添加文本到向量数据库"""
        try:
            # 分割文本
            split_texts = self.text_splitter.split_texts(texts)
            logger.info(f"文本分割完成，共{len(split_texts)}个片段")
            
            # 添加到向量数据库
            if isinstance(self.vector_db, Chroma):
                self.vector_db.add_texts(split_texts, metadatas)
                logger.info("文本已添加到Chroma数据库")
            elif isinstance(self.vector_db, FAISS):
                self.vector_db.add_texts(split_texts, metadatas)
                # 保存FAISS索引
                faiss_index_path = settings.VECTOR_DB_DIR / "faiss"
                self.vector_db.save_local(str(faiss_index_path))
                logger.info("文本已添加到FAISS数据库")
            
            logger.info(f"成功添加{len(split_texts)}个文本片段到向量数据库")
            
        except Exception as e:
            logger.error(f"添加文本失败: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """相似性搜索"""
        try:
            k = k or settings.TOP_K_RETRIEVAL
            results = self.vector_db.similarity_search(query, k=k)
            logger.info(f"相似性搜索完成，返回{len(results)}个结果")
            return results
            
        except Exception as e:
            logger.error(f"相似性搜索失败: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """带分数的相似性搜索"""
        try:
            k = k or settings.TOP_K_RETRIEVAL
            results = self.vector_db.similarity_search_with_score(query, k=k)
            logger.info(f"带分数的相似性搜索完成，返回{len(results)}个结果")
            return results
            
        except Exception as e:
            logger.error(f"带分数的相似性搜索失败: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """获取集合统计信息"""
        try:
            if isinstance(self.vector_db, Chroma):
                try:
                    collection = self.vector_db._collection
                    if collection and hasattr(collection, 'count'):
                        count = collection.count()
                        return {
                            "type": "chroma",
                            "document_count": count,
                            "embedding_dimension": "unknown"
                        }
                    else:
                        return {
                            "type": "chroma",
                            "document_count": "unknown",
                            "embedding_dimension": "unknown"
                        }
                except Exception as e:
                    logger.warning(f"获取Chroma统计信息失败: {e}")
                    return {
                        "type": "chroma",
                        "document_count": "error",
                        "embedding_dimension": "error"
                    }
            elif isinstance(self.vector_db, FAISS):
                try:
                    index = self.vector_db.index
                    return {
                        "type": "faiss",
                        "document_count": index.ntotal,
                        "embedding_dimension": index.d
                    }
                except Exception as e:
                    logger.warning(f"获取FAISS统计信息失败: {e}")
                    return {
                        "type": "faiss",
                        "document_count": "error",
                        "embedding_dimension": "error"
                    }
            else:
                return {
                    "type": "unknown",
                    "document_count": "unknown",
                    "embedding_dimension": "unknown"
                }
        except Exception as e:
            logger.error(f"获取集合统计信息失败: {e}")
            return {"error": str(e)}
