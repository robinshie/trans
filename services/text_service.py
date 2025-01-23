"""文本处理服务模块"""
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

class TextService:
    """文本处理服务类"""
    
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200
    
    @classmethod
    def split_into_chunks(cls, text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, 
                         chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
        """将文本分割成小块"""
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", ".", " "]
            )
            return splitter.split_text(text)
        except Exception as e:
            st.error(f"Error splitting text: {str(e)}")
            return []
