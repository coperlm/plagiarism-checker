from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import difflib
import hashlib
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB最大文件大小

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_hash(file_path):
    """计算文件的哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def extract_text_from_file(file_path):
    """从文件中提取文本"""
    # 这里只处理.txt文件，其他文件类型需要添加相应的库
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    else:
        # 实际应用中，你需要使用适当的库来处理不同类型的文件
        # 例如：PyPDF2处理PDF，python-docx处理DOCX等
        return "不支持的文件类型"

def check_similarity(text1, text2):
    """检查两个文本的相似度"""
    # 使用difflib库进行简单的相似度检查
    return difflib.SequenceMatcher(None, text1, text2).ratio()

def find_similar_sections(text1, text2):
    """寻找文本中的相似部分"""
    # 将文本分割成段落
    paragraphs1 = re.split(r'\n\s*\n', text1)
    paragraphs2 = re.split(r'\n\s*\n', text2)
    
    similar_sections = []
    
    # 计算每段的相似度
    for i, p1 in enumerate(paragraphs1):
        if len(p1.strip()) < 10:  # 忽略太短的段落
            continue
            
        for j, p2 in enumerate(paragraphs2):
            if len(p2.strip()) < 10:
                continue
                
            similarity = difflib.SequenceMatcher(None, p1, p2).ratio()
            if similarity > 0.7:  # 相似度阈值
                similar_sections.append({
                    'text1': p1,
                    'text2': p2,
                    'similarity': similarity,
                    'index1': i,
                    'index2': j
                })
    
    return similar_sections

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    if 'file1' not in request.files or 'file2' not in request.files:
        flash('请上传两个文件进行比较')
        return redirect(request.url)
        
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # 检查文件是否选择
    if file1.filename == '' or file2.filename == '':
        flash('未选择文件')
        return redirect(request.url)
    
    # 检查文件类型
    if not allowed_file(file1.filename) or not allowed_file(file2.filename):
        flash('文件类型不被支持')
        return redirect(request.url)
    
    # 安全地保存文件
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename1 = timestamp + "_1_" + secure_filename(file1.filename)
    filename2 = timestamp + "_2_" + secure_filename(file2.filename)
    
    filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    
    file1.save(filepath1)
    file2.save(filepath2)
    
    # 提取文本
    text1 = extract_text_from_file(filepath1)
    text2 = extract_text_from_file(filepath2)
    
    # 计算总体相似度
    overall_similarity = check_similarity(text1, text2)
    
    # 查找相似段落
    similar_sections = find_similar_sections(text1, text2)
    
    # 保存结果到会话
    result = {
        'file1': file1.filename,
        'file2': file2.filename,
        'overall_similarity': overall_similarity,
        'similar_sections': similar_sections
    }
    
    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
