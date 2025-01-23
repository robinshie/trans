import streamlit as st
from langchain.llms import Ollama
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
    """List available Ollama models"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        return [
            line.split()[0]
            for line in result.stdout.strip().split("\n")
            if line.strip() and line.split()[0] != "NAME"
        ]
    except FileNotFoundError:
        return [ModelConfig.get_error('file_not_found')]
    except subprocess.CalledProcessError as e:
        return [ModelConfig.get_error('list_error', error=e.stderr.strip())]

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
        api_key = os.environ.get("OPENAI_API_KEY")
        return query_gpt4(prompt, api_key, self.model_name) if api_key else self.config['error_message']

class OllamaModel(BaseModel):
    """Ollama模型类"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.config = ModelConfig.get_model_config('ollama')

    def generate_response(self, prompt: str) -> str:
        try:
            llm = Ollama(model=self.model_name)
            return llm(prompt)
        except Exception as e:
            st.error(ModelConfig.get_error('api_error', model='Ollama', error=str(e)))
            return self.config['error_message']

class DeepSeekModel(BaseModel):
    """DeepSeek模型类"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.config = ModelConfig.get_model_config('deepseek')

    def generate_response(self, prompt: str) -> str:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        return query_deepseek(prompt, api_key, self.model_name) if api_key else self.config['error_message']
