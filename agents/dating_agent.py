"""
约会指南智能体模块
"""
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from core.llm_manager import LLMManager
from core.vector_store import VectorStore
from tools.web_search import WebSearchTool
from utils.logger import get_logger

logger = get_logger(__name__)

class DatingAgent:
    """约会指南智能体"""
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.vector_store = VectorStore()
        self.web_search = WebSearchTool()
        self.qa_chain = None
        self._initialize()
    
    def _initialize(self):
        """初始化智能体"""
        try:
            # 创建问答链
            self._create_qa_chain()
            
            # 初始化知识库
            self._initialize_knowledge_base()
            
            logger.info("约会指南智能体初始化完成")
            
        except Exception as e:
            logger.error(f"智能体初始化失败: {e}")
            raise
    
    def _create_qa_chain(self):
        """创建问答链"""
        try:
            # 创建提示模板
            prompt_template = """你是一个专业的七夕约会规划师。基于以下上下文信息，为用户提供详细、实用的约会建议。

上下文信息:
{context}

用户问题: {question}

请提供:
1. 约会主题和氛围建议
2. 具体活动安排
3. 时间规划建议
4. 地点推荐
5. 注意事项和贴心提示

请用温暖、专业的语气回答，确保建议实用且浪漫。如果上下文信息不足，请基于你的专业知识提供建议。

约会规划师:"""

            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # 创建检索问答链 - 使用LLM管理器的LLM实例
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm_manager.get_llm_for_rag(),
                chain_type="stuff",
                retriever=self.vector_store.vector_db.as_retriever(
                    search_kwargs={"k": 5}
                ),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True
            )
            
            logger.info("问答链创建成功")
            
        except Exception as e:
            logger.error(f"创建问答链失败: {e}")
            raise
    
    def _initialize_knowledge_base(self):
        """初始化知识库"""
        try:
            # 检查向量数据库是否已有内容
            stats = self.vector_store.get_collection_stats()
            
            if stats.get("document_count", 0) == 0:
                logger.info("知识库为空，开始初始化基础约会知识...")
                
                # 添加基础约会知识
                self._add_basic_dating_knowledge()
                
                # 搜索并添加最新的约会信息
                self._search_and_add_dating_info()
                
                logger.info("知识库初始化完成")
            else:
                logger.info(f"知识库已有{stats.get('document_count', 0)}个文档")
                
        except Exception as e:
            logger.error(f"初始化知识库失败: {e}")
    
    def _add_basic_dating_knowledge(self):
        """添加基础约会知识"""
        basic_knowledge = [
            {
                "content": """
                七夕节是中国传统的情人节，起源于牛郎织女的美丽传说。这一天，情侣们会通过各种方式表达爱意，创造浪漫的回忆。

                浪漫约会的基本要素：
                1. 精心准备：提前规划，注意细节
                2. 个性化：根据对方的喜好定制
                3. 氛围营造：灯光、音乐、装饰等
                4. 惊喜元素：意想不到的小惊喜
                5. 情感表达：真诚的言语和行动
                """,
                "metadata": {"type": "basic_knowledge", "category": "dating_fundamentals"}
            },
            {
                "content": """
                经典约会活动推荐：
                1. 烛光晚餐：选择浪漫餐厅，营造温馨氛围
                2. 电影约会：选择爱情片或对方喜欢的类型
                3. 户外活动：公园散步、野餐、看星星
                4. 手工DIY：一起制作手工艺品或烹饪
                5. 惊喜礼物：精心挑选有意义的礼物
                6. 旅行约会：短途旅行，创造共同回忆
                """,
                "metadata": {"type": "basic_knowledge", "category": "dating_activities"}
            },
            {
                "content": """
                约会注意事项：
                1. 时间安排：合理安排时间，避免过于紧凑
                2. 预算控制：根据经济能力制定计划
                3. 天气考虑：关注天气预报，准备备选方案
                4. 交通便利：选择交通便利的地点
                5. 安全第一：注意人身和财产安全
                6. 尊重对方：考虑对方的感受和意愿
                """,
                "metadata": {"type": "basic_knowledge", "category": "dating_tips"}
            }
        ]
        
        # 转换为Document对象
        documents = []
        for item in basic_knowledge:
            doc = Document(
                page_content=item["content"],
                metadata=item["metadata"]
            )
            documents.append(doc)
        
        # 添加到向量数据库
        self.vector_store.add_documents(documents)
        logger.info("基础约会知识添加完成")
    
    def _search_and_add_dating_info(self):
        """搜索并添加约会信息"""
        try:
            # 搜索约会相关信息
            search_queries = [
                "七夕约会创意",
                "浪漫约会地点",
                "情侣约会活动",
                "约会礼物推荐"
            ]
            
            for query in search_queries:
                logger.info(f"搜索: {query}")
                results = self.web_search.search_dating_ideas(query)
                
                if results:
                    # 转换为Document对象
                    documents = []
                    for result in results[:3]:  # 每个查询取前3个结果
                        content = f"标题: {result['title']}\n\n内容: {result['snippet']}\n\n来源: {result['url']}"
                        doc = Document(
                            page_content=content,
                            metadata={
                                "type": "web_search",
                                "category": "dating_ideas",
                                "source": result["source"],
                                "url": result["url"],
                                "relevance_score": result["relevance_score"]
                            }
                        )
                        documents.append(doc)
                    
                    # 添加到向量数据库
                    if documents:
                        self.vector_store.add_documents(documents)
                        logger.info(f"添加{len(documents)}个搜索结果到知识库")
                
        except Exception as e:
            logger.error(f"搜索并添加约会信息失败: {e}")
    
    def plan_dating(self, user_query: str) -> Dict[str, Any]:
        """规划约会"""
        try:
            logger.info(f"收到用户查询: {user_query}")
            
            # 首先使用RAG系统检索相关知识
            logger.info("🔍 使用RAG系统检索相关知识...")
            relevant_docs = self.vector_store.similarity_search(user_query, k=5)
            
            if relevant_docs:
                logger.info(f"✅ 找到{len(relevant_docs)}个相关文档")
                
                # 构建包含检索内容的提示
                context_info = "\n\n".join([doc.page_content for doc in relevant_docs])
                enhanced_prompt = f"""
基于以下检索到的约会知识，为用户提供详细的约会规划：

检索到的知识：
{context_info}

用户需求：{user_query}

请提供：
1. 约会主题和氛围建议
2. 具体活动安排
3. 时间规划建议
4. 地点推荐
5. 注意事项和贴心提示

请用温暖、专业的语气回答，确保建议实用且浪漫。
"""
                
                # 使用LLM生成回答
                logger.info("🤖 基于检索内容生成回答...")
                answer = self.llm_manager.generate(enhanced_prompt)
                
                result = {
                    "answer": answer,
                    "source_documents": [],
                    "search_results": [],
                    "rag_used": True
                }
                
                # 添加源文档信息
                for doc in relevant_docs:
                    result["source_documents"].append({
                        "content": doc.page_content[:200] + "...",
                        "metadata": doc.metadata
                    })
                
                logger.info("✅ RAG系统回答生成完成")
                
            else:
                logger.info("⚠️ 未找到相关文档，直接使用LLM生成...")
                answer = self.llm_manager.generate(user_query)
                
                result = {
                    "answer": answer,
                    "source_documents": [],
                    "search_results": [],
                    "rag_used": False
                }
            
            # 如果RAG结果不够详细，进行网络搜索补充
            if len(result["answer"]) < 300:
                logger.info("🔍 RAG结果不够详细，进行网络搜索补充...")
                search_results = self.web_search.search_dating_ideas(user_query)
                result["search_results"] = search_results[:3]
                
                # 基于搜索结果生成补充建议
                if search_results:
                    enhanced_answer = self._enhance_answer_with_search(
                        result["answer"], search_results
                    )
                    result["answer"] = enhanced_answer
            
            logger.info("🎯 约会规划完成")
            return result
                
        except Exception as e:
            logger.error(f"规划约会失败: {e}")
            return {
                "answer": f"抱歉，规划约会时出现错误: {str(e)}",
                "source_documents": [],
                "search_results": [],
                "rag_used": False
            }
    
    def _enhance_answer_with_search(self, original_answer: str, search_results: List[Dict[str, Any]]) -> str:
        """基于搜索结果增强回答"""
        try:
            # 构建增强提示
            search_context = "\n\n".join([
                f"搜索结果 {i+1}:\n标题: {result['title']}\n内容: {result['snippet']}"
                for i, result in enumerate(search_results)
            ])
            
            enhancement_prompt = f"""
基于以下搜索结果，请为原有的约会建议提供更详细、更实用的补充信息：

原有建议：
{original_answer}

搜索结果：
{search_context}

请提供：
1. 具体的实施建议
2. 更多创意选择
3. 实用的注意事项
4. 个性化定制建议

请保持温暖、专业的语气，确保建议实用且浪漫。
"""
            
            # 使用LLM生成增强回答
            enhanced_answer = self.llm_manager.generate(enhancement_prompt)
            
            # 合并原有回答和增强内容
            final_answer = f"{original_answer}\n\n💡 补充建议：\n{enhanced_answer}"
            
            return final_answer
            
        except Exception as e:
            logger.error(f"增强回答失败: {e}")
            return original_answer
    
    def get_agent_status(self) -> Dict[str, Any]:
        """获取智能体状态"""
        try:
            return {
                "llm_ready": self.llm_manager.is_ready(),
                "vector_db_stats": self.vector_store.get_collection_stats(),
                "model_info": self.llm_manager.get_model_info(),
                "rag_chain_ready": self.qa_chain is not None
            }
        except Exception as e:
            logger.error(f"获取智能体状态失败: {e}")
            return {"error": str(e)}
