import streamlit as st
from langchain_ollama import OllamaLLM
from openai import OpenAI
import os
import yaml
import subprocess
import requests
from typing import Dict, List, Optional

class ModelConfig:
    """模型配置管理类"""
    
    # 加载配置
    _config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(_config_path, 'r', encoding='utf-8') as f:
        _config = yaml.safe_load(f)

    @classmethod
    def get_error(cls, key: str, **kwargs) -> str:
        """获取错误消息"""
        return cls._config['errors'].get(key, "Unknown error.").format(**kwargs)

    @classmethod
    def get_model_config(cls, model_type: str) -> Dict:
        """获取模型配置"""
        return cls._config['models'].get(model_type, {})

    @classmethod
    def get_config(cls) -> Dict:
        """获取配置"""
        return cls._config

def query_deepseek(prompt: str, api_key: str, model_name: str) -> str:
    """Query DeepSeek model"""
    try:
        config = ModelConfig.get_model_config('deepseek')
        response = requests.post(
            config['api_url'],
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_name,
                "messages": [
                    {"role": "system", "content": config['system_prompt']},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(ModelConfig.get_error('api_error', model='DeepSeek', error=str(e)))
        return ""

def list_ollama_models() -> List[str]:
    """获取可用的Ollama模型列表"""
    try:
        config = ModelConfig.get_config()
        if 'ollama' not in config.get('models', {}):
            st.error(ModelConfig.get_error('file_not_found'))
            return []
        
        models = config['models']['ollama'].get('available_models', [])
        return models
    except Exception as e:
        st.error(ModelConfig.get_error('list_error', error=str(e)))
        return []

def get_available_models(manufacturer: str) -> List[str]:
    """获取指定厂商的可用模型列表"""
    if manufacturer == "Ollama":
        return list_ollama_models()
    elif manufacturer == "OpenAI":
        return ModelConfig.get_model_config('openai').get('available_models', [])
    elif manufacturer == "DeepSeek":
        return ModelConfig.get_model_config('deepseek').get('available_models', [])
    return []

def get_api_key(manufacturer: str) -> Optional[str]:
    """获取API密钥"""
    if manufacturer == "OpenAI":
        return os.getenv("OPENAI_API_KEY")
    elif manufacturer == "DeepSeek":
        return os.getenv("DEEPSEEK_API_KEY")
    return None

def query_gpt4(prompt: str, api_key: str, model_name: str) -> str:
    """Query GPT-4 model from OpenAI"""
    try:
        config = ModelConfig.get_model_config('openai')
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": config['system_prompt']},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(ModelConfig.get_error('api_error', model='GPT-4', error=str(e)))
        return ""

class ModelFactory:
    """模型工厂类"""
    
    @staticmethod
    def get_model(model_choice: Dict[str, str]) -> 'BaseModel':
        """获取模型实例"""
        model_map = {
            "OpenAI": OpenAIModel,
            "Ollama": OllamaModel,
            "DeepSeek": DeepSeekModel
        }
        model_class = model_map.get(model_choice['model_frame'], BaseModel)
        return model_class(model_choice['model_name'])

class BaseModel:
    """基础模型类"""
    def generate_response(self, prompt: str) -> str:
        return ModelConfig.get_error('base')

class OpenAIModel(BaseModel):
    """OpenAI模型类"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.config = ModelConfig.get_model_config('openai')

    def generate_response(self, prompt: str) -> str:
        api_key = get_api_key("OpenAI")
        return query_gpt4(prompt, api_key, self.model_name) if api_key else self.config['error_message']

class OllamaModel(BaseModel):
    """Ollama模型类"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.config = ModelConfig.get_model_config('ollama')

    def generate_response(self, prompt: str) -> str:
        try:
            llm = OllamaLLM(model=self.model_name)
            return llm.invoke(prompt)
        except Exception as e:
            st.error(ModelConfig.get_error('api_error', model='Ollama', error=str(e)))
            return self.config['error_message']

class DeepSeekModel(BaseModel):
    """DeepSeek模型类"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.config = ModelConfig.get_model_config('deepseek')

    def generate_response(self, prompt: str) -> str:
        api_key = get_api_key("DeepSeek")
        return query_deepseek(prompt, api_key, self.model_name) if api_key else self.config['error_message']
