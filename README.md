# 文本查重系统

这是一个简单的Python文本查重系统，能够比较两个文档之间的相似度。

## 功能特点

- 支持多种文件格式（.txt, .pdf, .doc, .docx）
- 可视化相似度结果显示
- 高亮显示相似文本段落
- 现代化的Web界面

## 安装与运行

### 前提条件

- Python 3.7 或更高版本
- pip 包管理工具

### 安装依赖

```
pip install -r requirements.txt
```

### 运行应用

方法1: 直接运行批处理文件
```
start.bat
```

方法2: 使用命令行
```
python app.py
```

然后在浏览器中访问: http://localhost:5000

## 使用方法

1. 打开浏览器访问 http://localhost:5000
2. 上传两个需要比较的文件
3. 点击"开始查重"按钮
4. 查看结果页面显示的相似度分析

## 技术栈

- Python Flask - Web框架
- Bootstrap 5 - 前端UI库
- Werkzeug - WSGI工具库
- PyPDF2/python-docx - 文档处理库

## 注意事项

- 默认情况下，上传文件大小限制为16MB
- 当前支持的文件类型为：.txt, .pdf, .doc, .docx
- 对于非TXT格式的文件，可能需要安装额外的依赖项
