"""HTML模板管理模块"""

class ChatTemplates:
    """聊天界面HTML模板"""
    
    @staticmethod
    def message(role: str, content: str) -> str:
        """生成单条消息的HTML"""
        safe_content = content.replace("\n", "<br>")
        
        templates = {
            "user": (
                "<div style='margin-bottom:10px; padding:8px; border-radius:5px;"
                "background-color:#333; color:#EEE;'>"
                "<strong style='color:#C8D8FF;'>👤 User:</strong> "
                f"<span>{safe_content}</span>"
                "</div>"
            ),
            "assistant": (
                "<div style='margin-bottom:10px; padding:8px; border-radius:5px;"
                "background-color:#2A2A2A; color:#EEE;'>"
                "<strong style='color:#6F6;'>🤖 Assistant:</strong> "
                f"<span>{safe_content}</span>"
                "</div>"
            )
        }
        
        return templates.get(role, (
            "<div style='margin-bottom:10px; padding:8px; border-radius:5px;"
            "background-color:#444; color:#EEE;'>"
            f"<strong>{role.capitalize()}:</strong> "
            f"<span>{safe_content}</span>"
            "</div>"
        ))

    @staticmethod
    def chat_container(content: str = "", height: int = 1024) -> str:
        """生成聊天容器HTML"""
        if not content:
            content = "<p style='color:#AAA;'>No messages yet.</p>"
            
        return (
            f"<div id='chat-container' style='height:{height}px; overflow-y:auto; "
            "border:1px solid #444; background-color:#222; padding:10px;'>"
            f"{content}"
            "</div>"
        )

    @staticmethod
    def export_page(messages_html: str) -> str:
        """生成导出页面的HTML"""
        return f"""
            <html>
            <head>
                <meta charset='utf-8'/>
                <title>Chat Export</title>
            </head>
            <body style='background-color:#222; color:#EEE; font-family:Arial;'>
                <div style='width:80%; margin:0 auto; padding:10px;'>
                    <h2 style='color:#FFF;'>Exported Chat Conversation</h2>
                    {messages_html}
                </div>
            </body>
            </html>
        """
