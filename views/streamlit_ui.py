"""Streamlit UI组件模块"""
import os
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import webbrowser
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from services.file_service import FileService
from views.html_templates import ChatTemplates
from models.ModelFactory import list_ollama_models

class StreamlitUI:
    """Streamlit UI管理类"""
    
    @staticmethod
    def setup_sidebar() -> Tuple[Dict[str, str], List, str, object]:
        """设置侧边栏"""
        # 模型选择
        model_choice = StreamlitUI.model_selection()
        
        # 文件管理
        st.sidebar.header("📄 File Management")
        uploaded_files = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
        selected_file = st.sidebar.selectbox(
            "Select a file to view",
            [file.name for file in uploaded_files] if uploaded_files else []
        )

        # 导出部分
        st.sidebar.subheader("Export Conversation")
        messages_html = "".join(
            ChatTemplates.message(msg["role"], msg["content"])
            for msg in st.session_state.get("chat_history", [])
        )
        export_html = ChatTemplates.export_page(messages_html)
        st.sidebar.download_button(
            label="Download Conversation as HTML",
            data=export_html,
            file_name="conversation.html",
            mime="text/html"
        )

        # 图片上传
        st.sidebar.subheader("📷 Image Upload")
        image_files = st.sidebar.file_uploader(
            "Upload Image (PNG, JPG, JPEG)", 
            type=["png", "jpg", "jpeg"]
        )
        
        # 快速链接
        StreamlitUI.setup_quick_links()
        
        return model_choice, uploaded_files, selected_file, image_files

    @staticmethod
    def model_selection() -> Dict[str, str]:
        """模型选择界面"""
        st.sidebar.header("🤖 Model Selection")
        manufacturer = st.sidebar.selectbox(
            "Select Manufacturer",
            ["Ollama", "OpenAI", "DeepSeek"]
        )
        
        model_info = {
            "model_frame": manufacturer,
            "model_name": None,
            "api_key": None
        }
        
        if manufacturer == "Ollama":
            ollama_models = list_ollama_models()
            model_info["model_name"] = st.sidebar.selectbox(
                "Select Ollama Model",
                ollama_models
            )
        elif manufacturer == "OpenAI":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                api_key = st.sidebar.text_input(
                    "Enter OpenAI API Key:",
                    type="password"
                )
            model_info.update({
                "model_name": st.sidebar.selectbox(
                    "Select OpenAI Model",
                    ["gpt-4", "gpt-3.5-turbo", "gpt-4o"]
                ),
                "api_key": api_key
            })
        elif manufacturer == "DeepSeek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                api_key = st.sidebar.text_input(
                    "Enter DeepSeek API Key:",
                    type="password"
                )
            model_info.update({
                "model_name": "deepseek-chat",
                "api_key": api_key
            })
        
        return model_info

    @staticmethod
    def setup_quick_links():
        """设置快速链接"""
        html_path = Path(__file__).parent.parent / "index.html"
        if not html_path.exists():
            st.error("文件预览未找到！")
            return
            
        st.sidebar.button(
            "📂 Open Web", 
            on_click=StreamlitUI.safe_open_web,
            args=([
                f"file://{html_path.resolve()}",
                "https://www.google.com", 
                "https://translate.google.com",
                "https://chatgpt.com/?oai-dm=1"
            ],)
        )

    @staticmethod
    def safe_open_web(urls: List[str]):
        """安全打开网页"""
        try:
            for url in urls:
                webbrowser.open(url)
        except Exception as e:
            st.error(f"打开失败: {str(e)}")

    @staticmethod
    def render_latex():
        """渲染LaTeX编辑器 - 左侧输入，右侧实时预览"""
        st.subheader("✍️ LaTeX Editor")
        
        if 'latex_text' not in st.session_state:
            st.session_state.latex_text = ""
            
        def on_latex_change():
            st.session_state.latex_text = st.session_state.latex_input
        
        # 创建两列布局
        col1, col2 = st.columns(2)
        
        # 左侧输入区
        with col1:
            latex_input = st.text_area(
                "Enter LaTeX code:",
                height=200,
                key="latex_input",
                on_change=on_latex_change,
                value=st.session_state.latex_text
            )
        
        # 右侧预览区
        with col2:
            st.markdown("### Preview")
            try:
                st.latex(st.session_state.latex_text)
            except Exception as e:
                st.error(f"Error rendering LaTeX: {str(e)}")

    @staticmethod
    def render_pdf_view(uploaded_files: List, selected_file: str, image_file: Optional[object]):
        """渲染PDF预览"""
        if selected_file:
            for file in uploaded_files:
                if file.name == selected_file:
                    temp_path = FileService.save_temp_pdf(file)
                    if temp_path:
                        pdf_viewer(temp_path, height=1064)
                        os.unlink(temp_path)  # 清理临时文件
                        break

        if image_file:
            with st.expander("📷 Extracted Text from Image", expanded=False):
                image_text = FileService.extract_text_from_image(image_file)
                st.text_area("", value=image_text, height=150)

    @staticmethod
    def render_chat(chat_history: List[Dict]):
        """渲染聊天界面"""
        if chat_history:
            messages_html = "".join(
                ChatTemplates.message(msg["role"], msg["content"])
                for msg in chat_history
            )
            container_html = ChatTemplates.chat_container(messages_html)
        else:
            container_html = ChatTemplates.chat_container()
        
        st.markdown(container_html, unsafe_allow_html=True)

    @staticmethod
    def clear_chat_history():
        """清空聊天历史和输入"""
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        if "user_input" in st.session_state:
            st.session_state.user_input = ""
        if "latex_text" in st.session_state:
            st.session_state.latex_text = ""
        st.rerun()

    def render_chat_interface(self):
        """渲染聊天界面"""
        st.title("💬 Chat Interface")
        
        # 添加快捷键
        st.markdown("""
        <script>
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'l') {
                e.preventDefault();
                window.location.href = window.location.pathname + '?clear=1';
            }
        });
        </script>
        """, unsafe_allow_html=True)
        
        # 检查是否需要清空历史
        params = st.experimental_get_query_params()
        if params.get("clear"):
            self.clear_chat_history()
            st.experimental_set_query_params()
        
        # 显示聊天历史
        for msg in st.session_state.get("chat_history", []):
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "user":
                container_html = ChatTemplates.user_container(content)
            else:
                container_html = ChatTemplates.chat_container(content)
            
            st.markdown(container_html, unsafe_allow_html=True)
