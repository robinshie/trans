import os
import yaml
from typing import List, Dict

class CausalPromptFactory:
    """提示词工厂类，用于构建不同场景的提示词"""
    
    def __init__(self):
        """初始化提示词工厂"""
        # 加载提示词配置
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            self.prompts = yaml.safe_load(f)['prompts']
    
    def build_query_prompt(self, query: str, texts: List[str]) -> str:
        """
        构建查询提示词
        
        Args:
            query: 用户查询
            texts: 相关文本列表
            
        Returns:
            str: 完整的提示词
        """
        # 系统提示词
        system_prompt = self.prompts['system']
        
        # 合并所有文本
        text_content = "\n\n".join(texts) if texts else "没有提供文本内容。"
        
        # 查询提示词
        query_prompt = self.prompts['query'].format(
            text=text_content,
            query=query
        )
        
        return f"{system_prompt}\n\n{query_prompt}"
    
    def build_followup_prompt(self, query: str, texts: List[str], 
                            history: List[Dict[str, str]]) -> str:
        """
        构建后续对话提示词
        
        Args:
            query: 用户查询
            texts: 相关文本列表
            history: 对话历史
            
        Returns:
            str: 完整的提示词
        """
        # 系统提示词
        system_prompt = self.prompts['system']
        
        # 合并所有文本
        text_content = "\n\n".join(texts) if texts else "没有提供文本内容。"
        
        # 格式化对话历史
        history_text = ""
        for msg in history:
            if msg["role"] == "user":
                history_text += f"用户: {msg['content']}\n"
            else:
                history_text += f"助手: {msg['content']}\n"
        
        # 后续对话提示词
        followup_prompt = self.prompts['followup'].format(
            text=text_content,
            history=history_text,
            query=query
        )
        
        return f"{system_prompt}\n\n{followup_prompt}"

class AcademicReadingAssistant:
    """学术文献分析系统"""
    
    # 加载提示词配置
    _prompt_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")
    with open(_prompt_path, 'r', encoding='utf-8') as f:
        _prompts = yaml.safe_load(f)['academic']
    
    @classmethod
    def build_context_prompt(cls, pdf_content: str, language: str = "中文") -> str:
        """构建上下文分析提示"""
        lang = "zh" if language == "中文" else "en"
        return cls._prompts['context'][lang].format(content=pdf_content)
    
    @classmethod
    def build_query_prompt(cls, question: str, context_tags: list, language: str = "中文") -> str:
        """构建问题分析提示"""
        lang = "zh" if language == "中文" else "en"
        context = ", ".join(context_tags)
        return cls._prompts['query'][lang].format(
            context=context,
            question=question
        )
    
    @classmethod
    def build_validation_prompt(cls, response: str, source_materials: str, language: str = "中文") -> str:
        """构建验证提示"""
        lang = "zh" if language == "中文" else "en"
        return cls._prompts['validation'][lang].format(
            source=source_materials,
            response=response
        )
    
    @classmethod
    def build_followup_prompt(cls, history: str, language: str = "中文") -> str:
        """构建追问提示"""
        lang = "zh" if language == "中文" else "en"
        return cls._prompts['followup'][lang].format(history=history)