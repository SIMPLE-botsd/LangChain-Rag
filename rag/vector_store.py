import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger_handler import logger
from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
import os
from utils.file_handler import txt_loader,pdf_loader
from langchain_core.documents import Document
from utils.file_handler import listdir_with_allowed_type
from utils.file_handler import get_file_md5


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_config["collection_name"],
            embedding_function = embed_model,
            persist_directory = chroma_config["persist_directory"],
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_config["chunk_size"],
            chunk_overlap = chroma_config["chunk_overlap"],
            separators = chroma_config["separators"],
            length_function = len,
        )


    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs = {
                "k": chroma_config["k"],
            }
        )

    def load_documents(self):
        """
        从数据文件夹读取数据文件，转为向量存入向量数据库
        要计算文件的md5值，如果文件md5值与向量数据库中已有的文件md5值相同，则不进行存储
        :return: 返回向量数据库中存储的文件数量
        """
        def check_md5(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                # 如果md5_hex_store文件不存在，则创建文件
                open(get_abs_path(chroma_config["md5_hex_store"]), "w",encoding="utf-8").close()
                return False     # MD5值不存在，返回False
            with open(get_abs_path(chroma_config["md5_hex_store"]), "r",encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True     # MD5值存在，返回True
                return False     # MD5值不存在，返回False

        def save_md5(md5_for_save: str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), "a",encoding="utf-8") as f:
                f.write(md5_for_save + "\n")

        def get_file_documents(file_path: str) -> list[Document]:
            if file_path.endswith(".txt"):
                return txt_loader(file_path)
            elif file_path.endswith(".pdf"):
                return pdf_loader(file_path)
            else:
                return []


        allowed_file_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"]),
            )
        for file_path in allowed_file_path:
            # 获取文件的md5值
            md5_hex = get_file_md5(file_path)
            if check_md5(md5_hex):
                logger.info(f"[加载知识库] 文件{file_path}已存在，跳过")
                continue
            try:    # 获取文件的文档
                documents: list[Document] = get_file_documents(file_path)
                if not documents:
                    logger.warning(f"[加载知识库] 文件{file_path}读取失败 没有读取到文档，跳过")
                    continue
                # 将文件的文档分割为块
                split_documents: list[Document] = self.spliter.split_documents(documents)
                if not split_documents:
                    logger.warning(f"[加载知识库] 文件{file_path}分割失败 没有分割到文档，跳过")
                    continue

                # 将文件的文档转为向量存入向量数据库
                self.vector_store.add_documents(split_documents)
                # 保存文件的md5值
                save_md5(md5_hex)
                logger.info(f"[加载知识库] 文件{file_path}加载成功") 
            except Exception as e:
                # exc_info = True 打印异常堆栈信息 记录详细的异常信息
                logger.error(f"[加载知识库] 文件{file_path}读取失败 {str(e)},exc_info = True")
                continue

 
# if __name__ == "__main__":
#     vector_store_service = VectorStoreService()
#     vector_store_service.load_documents()
#     retriever = vector_store_service.get_retriever()
#     res =retriever.invoke("迷路")
#     for r in res:
#         print(r.page_content)
#         print("-"*20)