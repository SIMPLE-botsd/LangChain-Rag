"""
 总结服务类： 用户提问 -> 向量数据库检索相关文档 -> 将检索到的文档与用户问题一起输入生成模型 让模型总结回复 -> 返回答案
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt
    

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()    
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()
        
    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain
    
    def retriever_docs(self,query: str) -> list[Document ]:
        return self.retriever.invoke(query)
    
    def rag_summarize(self,query: str) -> str:
        # 1. 检索相关文档
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【相关文档{counter}】:参考资料:{doc.page_content} | 参考元数据:{doc.metadata}\n"
            
        return self.chain.invoke({
            "input": query, 
            "context": context  ,
            }
        )
        
        
# if __name__ == '__main__':
#     rag = RagSummarizeService()
#     answer = rag.rag_summarize("小户型适合什么扫地机器人？")
#     print(answer)