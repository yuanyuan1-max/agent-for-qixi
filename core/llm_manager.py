"""
LLM管理器模块
"""
import os
from typing import Optional, List, Dict, Any
from pathlib import Path

from langchain.llms import HuggingFacePipeline
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    BitsAndBytesConfig
)
import torch

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMManager:
    """LLM管理器类"""
    
    def __init__(self):
        self.llm = None
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.use_openai = False
        self._initialize()
    
    def _initialize(self):
        """初始化LLM模型"""
        try:
            # 检查是否配置了OpenAI API
            if settings.OPENAI_API_KEY and settings.OPENAI_API_BASE:
                logger.info("检测到OpenAI API配置，使用ChatAnywhere API")
                self._init_openai()
                self.use_openai = True
            else:
                logger.info("使用本地LLaMA模型")
                self._init_local_llama()
                self.use_openai = False
                
        except Exception as e:
            logger.error(f"LLM模型初始化失败: {e}")
            raise
    
    def _init_openai(self):
        """初始化OpenAI API"""
        try:
            # 设置环境变量
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
            os.environ["OPENAI_API_BASE"] = settings.OPENAI_API_BASE
            
            # 创建OpenAI聊天模型
            self.llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0.7,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
            
            logger.info("OpenAI API初始化成功")
            
        except Exception as e:
            logger.error(f"OpenAI API初始化失败: {e}")
            raise
    
    def _init_local_llama(self):
        """初始化本地LLaMA模型"""
        try:
            logger.info(f"开始初始化本地LLM模型: {settings.MODEL_NAME}")
            
            # 检查是否有GPU
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"使用设备: {device}")
            
            # 设置量化配置（如果有GPU）
            if device == "cuda":
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=False,
                )
            else:
                bnb_config = None
            
            # 加载tokenizer
            logger.info("加载tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.MODEL_NAME,
                cache_dir=str(settings.MODEL_CACHE_DIR),
                trust_remote_code=True
            )
            
            # 设置pad_token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # 加载模型
            logger.info("加载模型...")
            if bnb_config:
                self.model = AutoModelForCausalLM.from_pretrained(
                    settings.MODEL_NAME,
                    cache_dir=str(settings.MODEL_CACHE_DIR),
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                    torch_dtype=torch.float16
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    settings.MODEL_NAME,
                    cache_dir=str(settings.MODEL_CACHE_DIR),
                    device_map="auto",
                    trust_remote_code=True,
                    torch_dtype=torch.float32
                )
            
            # 创建pipeline
            logger.info("创建pipeline...")
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.15,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # 创建LangChain LLM
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            self.llm = HuggingFacePipeline(
                pipeline=self.pipeline,
                callback_manager=callback_manager,
                verbose=True
            )
            
            logger.info("本地LLM模型初始化成功")
            
        except Exception as e:
            logger.error(f"本地LLM模型初始化失败: {e}")
            raise
    
    def generate(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
        """生成文本"""
        try:
            if not self.llm:
                raise RuntimeError("LLM模型未初始化")
            
            if self.use_openai:
                # 使用OpenAI API
                return self._generate_with_openai(prompt)
            else:
                # 使用本地LLaMA
                return self._generate_with_local_llama(prompt)
                
        except Exception as e:
            logger.error(f"文本生成失败: {e}")
            return f"生成失败: {str(e)}"
    
    def _generate_with_openai(self, prompt: str) -> str:
        """使用OpenAI API生成文本"""
        try:
            # 构建完整的提示
            full_prompt = self._build_prompt(prompt)
            
            # 使用OpenAI生成
            response = self.llm.invoke(full_prompt)
            
            # 清理响应
            cleaned_response = self._clean_response(str(response.content), prompt)
            
            logger.info(f"OpenAI API文本生成完成，长度: {len(cleaned_response)}")
            return cleaned_response
            
        except Exception as e:
            logger.error(f"OpenAI API生成失败: {e}")
            return f"OpenAI API生成失败: {str(e)}"
    
    def _generate_with_local_llama(self, prompt: str) -> str:
        """使用本地LLaMA生成文本"""
        try:
            # 构建完整的提示
            full_prompt = self._build_prompt(prompt)
            
            # 生成文本
            response = self.llm(full_prompt)
            
            # 清理响应
            cleaned_response = self._clean_response(response, prompt)
            
            logger.info(f"本地LLM文本生成完成，长度: {len(cleaned_response)}")
            return cleaned_response
            
        except Exception as e:
            logger.error(f"本地LLM生成失败: {e}")
            return f"本地LLM生成失败: {str(e)}"
    
    def _build_prompt(self, user_input: str) -> str:
        """构建提示词"""
        # 七夕约会指南的系统提示
        system_prompt = """你是一个专业的七夕约会规划师，擅长为情侣提供浪漫、有趣、个性化的约会建议。

你的任务是根据用户的需求，提供详细的约会规划，包括：
1. 约会主题和氛围
2. 具体活动安排
3. 时间规划
4. 地点推荐
5. 注意事项和建议

请用温暖、专业的语气回答，确保建议实用且浪漫。"""
        
        if self.use_openai:
            # OpenAI格式的提示
            return f"{system_prompt}\n\n用户需求: {user_input}"
        else:
            # 本地LLaMA格式的提示
            return f"{system_prompt}\n\n用户需求: {user_input}\n\n约会规划师:"
    
    def _clean_response(self, response: str, original_prompt: str) -> str:
        """清理响应文本"""
        # 移除原始提示
        if original_prompt in response:
            response = response.replace(original_prompt, "")
        
        # 移除系统提示
        system_prompt = "你是一个专业的七夕约会规划师"
        if system_prompt in response:
            response = response.replace(system_prompt, "")
        
        # 清理多余的空行和空格
        response = response.strip()
        
        return response
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        try:
            if self.use_openai:
                return {
                    "type": "openai",
                    "model": "gpt-4o",
                    "api_base": settings.OPENAI_API_BASE,
                    "provider": "ChatAnywhere"
                }
            else:
                return {
                    "type": "local",
                    "model_name": settings.MODEL_NAME,
                    "tokenizer_vocab_size": len(self.tokenizer) if self.tokenizer else 0,
                    "model_parameters": sum(p.numel() for p in self.model.parameters()) if self.model else 0,
                    "device": str(next(self.model.parameters()).device) if self.model else "unknown"
                }
        except Exception as e:
            logger.error(f"获取模型信息失败: {e}")
            return {"error": str(e)}
    
    def is_ready(self) -> bool:
        """检查模型是否准备就绪"""
        return self.llm is not None
    
    def get_llm_for_rag(self):
        """获取用于RAG的LLM实例"""
        """这个方法专门用于RAG系统，确保RAG能正常工作"""
        return self.llm
