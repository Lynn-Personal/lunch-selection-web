from flask import Flask, request, send_file, render_template_string, flash, redirect, url_for
import os
import tempfile
import io
import re
from werkzeug.utils import secure_filename
from fill_ppt import run_fill_ppt
import zipfile

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于flash消息

# 允许的文件类型
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_excel_file(filepath):
    """验证是否是有效的Excel文件"""
    try:
        # xlsx文件本质上是ZIP格式，先检查是否是有效的ZIP
        if not zipfile.is_zipfile(filepath):
            return False, "文件不是有效的Excel格式"
        
        # 再检查是否包含必要的Excel结构文件
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            # 检查是否有xl/workbook.xml（Excel文件必有）
            if 'xl/workbook.xml' not in zip_ref.namelist():
                return False, "文件结构不完整或不是有效的Excel文件"
        return True, ""
    except Exception as e:
        return False, f"文件验证失败: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            flash('没有文件部分')
            return redirect(request.url)
        file = request.files['file']
        # 获取用户选择的餐类型
        menu_type = request.form.get('menu_type', 'A')
        
        # 如果用户没有选择文件，浏览器也会提交一个空的文件部分
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 提取文件名中的日期部分
            match = re.match(r'([\d-]+)', filename)
            if match:
                date_str = match.group(1)
            else:
                date_str = "未知日期"
            output_filename = f"星辰班{menu_type}餐表（{date_str}）.pptx"
            
            # 保存上传的文件到临时目录
            temp_excel_path = None
            try:
                # 创建临时文件（先不写入）
                temp_file_obj = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
                temp_excel_path = temp_file_obj.name
                temp_file_obj.close()
                
                # 将上传的文件保存到临时位置
                file.save(temp_excel_path)
                
                # 验证Excel文件有效性
                is_valid, error_msg = is_valid_excel_file(temp_excel_path)
                if not is_valid:
                    flash(f'上传的文件无效: {error_msg}')
                    if os.path.exists(temp_excel_path):
                        os.unlink(temp_excel_path)
                    return redirect(request.url)
                
                # 创建临时输出目录
                with tempfile.TemporaryDirectory() as temp_output_dir:
                    # 调用fill_ppt生成PPT，传递菜单类型
                    output_path = run_fill_ppt(excel_path=temp_excel_path, output_dir=temp_output_dir, output_filename=output_filename, menu_type=menu_type)
                    # 读取PPT文件内容到内存
                    with open(output_path, 'rb') as f:
                        ppt_data = io.BytesIO(f.read())
                    ppt_data.seek(0)
                    # 返回生成的PPT文件
                    return send_file(ppt_data, as_attachment=True, download_name=output_filename, mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            except Exception as e:
                flash(f'处理文件时出错: {str(e)}')
                return redirect(request.url)
            finally:
                # 清理临时Excel文件
                if temp_excel_path and os.path.exists(temp_excel_path):
                    os.unlink(temp_excel_path)
        else:
            flash('只允许上传.xlsx文件')
            return redirect(request.url)
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>午餐选择PPT生成器</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
            .upload-form { border: 2px dashed #ccc; padding: 30px; text-align: center; }
            .form-row {
                display: flex;
                gap: 20px;
                align-items: center;
                justify-content: center;
                margin: 20px 0;
                flex-wrap: wrap;
            }
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
                flex: 1;
                min-width: 200px;
            }
            .form-group label {
                font-weight: bold;
                text-align: left;
            }
            .upload-form input[type="file"] { 
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .upload-form select {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                cursor: pointer;
            }
            .upload-form input[type="submit"] { 
                background-color: #4CAF50; 
                color: white; 
                padding: 12px 30px; 
                border: none; 
                cursor: pointer;
                border-radius: 4px;
                margin-top: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            .upload-form input[type="submit"]:hover {
                background-color: #45a049;
            }
            .flash { color: red; }
        </style>
    </head>
    <body>
        <h1>午餐选择PPT生成器</h1>
        <p>上传Excel文件，自动生成午餐安排PPT。</p>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul class="flash">
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        <form method="post" enctype="multipart/form-data" class="upload-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="file">选择Excel文件：</label>
                    <input type="file" id="file" name="file" accept=".xlsx" required>
                </div>
                <div class="form-group">
                    <label for="menu_type">选择餐类型：</label>
                    <select id="menu_type" name="menu_type">
                        <option value="A">A餐</option>
                        <option value="B">B餐</option>
                    </select>
                </div>
            </div>
            <input type="submit" value="生成PPT">
        </form>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    # 在生产环境中禁用debug模式
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))