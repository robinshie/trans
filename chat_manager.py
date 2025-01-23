"""聊天管理模块"""
from typing import Dict, List, Optional
import streamlit as st
from models.ModelFactory import ModelFactory
from models.CausalPromptFactory import AcademicReadingAssistant

class ChatManager:
    """聊天管理类"""
    
    @classmethod
    def initialize_state(cls):
        """初始化会话状态"""
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        
        if "mode" not in st.session_state:
            st.session_state["mode"] = "Chat Mode"
            
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

    @classmethod
    def handle_input(cls, user_input: str, model_choice: Dict[str, str], pdf_text: str) -> None:
        """处理用户输入"""
        if user_input:
            try:
                # 添加用户消息
                st.session_state["chat_history"].append({
                    "role": "user",
                    "content": user_input
                })
                
                # 构建提示
                prompt = AcademicReadingAssistant.build_query_prompt(
                    user_input, 
                    [pdf_text] if pdf_text else []
                )
                
                # 获取模型实例并生成响应
                model = ModelFactory.get_model(model_choice)
                response = model.generate_response(prompt)
                
                # 添加助手消息
                st.session_state["chat_history"].append({
                    "role": "assistant",
                    "content": response
                })
                
                # 清空输入
                st.session_state.user_input = ""
                
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")

    @classmethod
    def get_chat_history(cls) -> List[Dict]:
        """获取聊天历史"""
        return st.session_state.get("chat_history", [])
