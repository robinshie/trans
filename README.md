# Trans Project

一个基于AI的文档翻译和处理工具。

## 功能特点

- 支持多种文档格式（PDF、图片等）的文本提取
- 使用先进的AI模型进行翻译
- 提供友好的Web界面
- 支持OCR图片文字识别

## 环境要求

- Python >= 3.11
- CUDA支持（用于PyTorch GPU加速）
- Conda包管理器

## 安装步骤

1. 克隆项目：
```bash
git clone [项目地址]
cd trans
```

2. 创建并激活Conda环境：
```bash
conda env update -f environment.yml
conda activate trans
```

3. 配置环境变量：
创建`.env`文件并设置必要的API密钥：
```
OPENAI_API_KEY=your_api_key_here
```

## 运行应用

使用以下命令启动应用：

Linux/Mac:
```bash
bash run_linux.sh
```

Windows:
```bash
run_windows.bat
```

启动后，在浏览器中访问显示的地址（通常是 http://localhost:8501）

## 主要依赖

- PyTorch >= 2.1.0：深度学习框架
- EasyOCR >= 1.7.1：OCR文字识别
- Langchain >= 0.0.352：AI模型集成
- OpenAI >= 1.3.7：AI接口
- Streamlit >= 1.29.0：Web界面框架

## 使用说明

1. 在Web界面上传文档（支持PDF或图片格式）
2. 选择所需的翻译选项
3. 点击开始处理
4. 等待处理完成后查看结果

## 注意事项

- 请确保有足够的系统内存
- 对于大型文件，处理时间可能较长
- 使用GPU可以显著提升处理速度
