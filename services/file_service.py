"""文件处理服务模块"""
import os
from tempfile import NamedTemporaryFile
from typing import List, Optional, Tuple
import easyocr
from PyPDF2 import PdfReader
import pdfkit
import streamlit as st

class FileService:
    """文件处理服务类"""
    
    SUPPORTED_LANGUAGES = ['en', 'ch_sim']
    
    @classmethod
    def extract_text_from_image(cls, image_file) -> str:
        """从图片中提取文本"""
        try:
            reader = easyocr.Reader(cls.SUPPORTED_LANGUAGES)
            image_bytes = image_file.read()
            with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(image_bytes)
                temp_file_path = temp_file.name
            results = reader.readtext(temp_file_path, detail=0)
            os.unlink(temp_file_path)  # 清理临时文件
            return "\n".join(results)
        except Exception as e:
            st.error(f"Error extracting text from image: {str(e)}")
            return ""

    @staticmethod
    def extract_pdf_text(pdf_file) -> str:
        """从PDF文件中提取文本"""
        try:
            reader = PdfReader(pdf_file)
            pdf_text = "\n".join(
                page.extract_text()
                for page in reader.pages
                if page.extract_text()
            )
            return pdf_text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""

    @staticmethod
    def export_to_pdf(html_content: str) -> bytes:
        """将HTML内容转换为PDF"""
        try:
            config = pdfkit.configuration()
            return pdfkit.from_string(html_content, False, configuration=config)
        except Exception as e:
            st.error(f"Error converting to PDF: {str(e)}")
            return b""

    @staticmethod
    def save_temp_pdf(pdf_file) -> str:
        """保存临时PDF文件，返回临时文件路径"""
        try:
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_file.read())
                return temp_file.name
        except Exception as e:
            st.error(f"Error saving temporary PDF: {str(e)}")
            return ""
