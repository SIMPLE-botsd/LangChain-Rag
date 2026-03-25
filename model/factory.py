import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from utils.config_handler import rag_config


class BaseModelFactory(ABC):
    """AI模型工厂基类"""
    
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """生成模型实例的方法
        
        Returns:
            Optional[Embeddings | BaseChatModel]: 返回嵌入模型或聊天模型实例
        """
        pass


class ChatModelFactory(BaseModelFactory):
    """通义千问聊天模型工厂类"""
    
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """创建通义千问聊天模型实例
        
        Returns:
            ChatTongyi: 通义千问聊天模型实例
        """
        return ChatTongyi(model=rag_config["chat_model_name"])


class EmbeddingModelFactory(BaseModelFactory):
    """DashScope嵌入模型工厂类"""
    
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """创建DashScope嵌入模型实例
        
        Returns:
            DashScopeEmbeddings: DashScope嵌入模型实例
        """
        # 可以根据配置返回具体的嵌入模型
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])
    
    
# 创建工厂实例
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingModelFactory().generator() 