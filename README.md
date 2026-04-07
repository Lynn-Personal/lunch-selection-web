# 午餐选择PPT生成器 - Web版本

这是一个简化的Web应用版本的午餐选择PPT生成器。用户可以通过网页上传Excel文件，直接生成并下载PPT，而无需运行本地应用。

## 功能特性

- 🌐 基于Flask的Web界面
- 📤 文件上传和下载
- 📊 从Excel自动生成PPT
- 🚀 简化部署，无需本地安装

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python lunch_app_web.py
```

然后在浏览器中访问 `http://127.0.0.1:5000/` 上传Excel文件并生成PPT。

## 使用说明

1. 打开浏览器访问应用地址
2. 点击选择文件，上传包含午餐选择数据的Excel文件
3. 点击"生成PPT"按钮
4. 等待处理完成后，自动下载生成的PPT文件

## 技术栈

- Flask: Web框架
- pandas: 数据处理
- openpyxl: Excel文件读取
- python-pptx: PPT生成

## 注意事项

- 只支持.xlsx格式的Excel文件
- Excel文件需要包含特定格式的数据（参考原项目说明）
- 生成的PPT基于固定模板