from flask import Flask, request, send_file, render_template_string, flash, redirect, url_for
import os
import tempfile
import io
import re
from werkzeug.utils import secure_filename
from fill_ppt import run_fill_ppt

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于flash消息

# 允许的文件类型
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            flash('没有文件部分')
            return redirect(request.url)
        file = request.files['file']
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
            output_filename = f"星辰班A餐表（{date_str}）.pptx"
            
            # 保存上传的文件到临时目录
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                file.save(temp_file.name)
                temp_excel_path = temp_file.name

            try:
                # 创建临时输出目录
                with tempfile.TemporaryDirectory() as temp_output_dir:
                    # 调用fill_ppt生成PPT
                    output_path = run_fill_ppt(excel_path=temp_excel_path, output_dir=temp_output_dir, output_filename=output_filename)
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
                if os.path.exists(temp_excel_path):
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
            .upload-form { border: 2px dashed #ccc; padding: 20px; text-align: center; }
            .upload-form input[type="file"] { margin: 10px 0; }
            .upload-form input[type="submit"] { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
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
            <input type="file" name="file" accept=".xlsx" required>
            <br>
            <input type="submit" value="生成PPT">
        </form>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    # 在生产环境中禁用debug模式
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))