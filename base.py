"""主程序入口"""
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from typing import List, Dict, Optional
from services.file_service import FileService
from views.streamlit_ui import StreamlitUI
from chat_manager import ChatManager

def conversation_mode(model_choice: Dict[str, str], pdf_text: str) -> None:
    """学术文献解析对话模式"""
    ChatManager.initialize_state()
    StreamlitUI.render_chat(ChatManager.get_chat_history())
    
    # 输入处理
    st.text_input("Message", 
                 value=st.session_state.user_input,
                 key="user_input",
                 placeholder="Ask about the document...", 
                 label_visibility="collapsed",
                 on_change=lambda: ChatManager.handle_input(
                     st.session_state.user_input, 
                     model_choice, 
                     pdf_text
                 ))

def chat_mode(model_choice: Dict[str, str], uploaded_files: List,
              selected_file: str, image_files: object) -> None:
    """聊天模式界面"""
    # 布局
    left_panel, right_panel = st.columns([1, 1])

    # 左侧：PDF & 图像
    with left_panel:
        StreamlitUI.render_pdf_view(uploaded_files, selected_file, image_files)

    # 从PDF提取文本
    pdf_text = ""
    if selected_file and uploaded_files:
        for file in uploaded_files:
            if file.name == selected_file:
                pdf_text = FileService.extract_pdf_text(file)
                break

    # 右侧：Chat
    with right_panel:
        conversation_mode(model_choice, pdf_text)

def main() -> None:
    """主程序入口"""
    try:
        # 配置页面设置
        st.set_page_config(
            layout="wide",
            page_title="ChatPDF & LaTeX Interaction",
            initial_sidebar_state="expanded"
        )
        st.title("Interact with PDFs and LaTeX Content ")

        # 初始化状态
        ChatManager.initialize_state()
        
        # 设置界面
        model_choice, uploaded_files, selected_file, image_files = StreamlitUI.setup_sidebar()
        
        # 初始化模式选择的session state
        if "mode" not in st.session_state:
            st.session_state["mode"] = "Chat Mode"

        # 侧边栏模式选择
        mode = st.sidebar.radio(
            "Select Mode:",
            ["Chat Mode", "LaTeX Mode"],
            index=0,
            horizontal=True,
            key="mode_selector"
        )
        st.session_state["mode"] = mode
        
        if model_choice:
            # 根据模式显示不同界面
            if mode == "Chat Mode":
                chat_mode(model_choice, uploaded_files, selected_file, image_files)
            elif mode == "LaTeX Mode":
                StreamlitUI.render_latex()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()