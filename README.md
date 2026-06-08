# 午餐选择PPT生成器 - Web版本

这是一个基于Flask的Web应用，用于从Excel数据自动生成午餐安排PPT演示文稿。支持A餐和B餐两种菜单类型的独立生成。

## ✨ 功能特性

- 🌐 **Web界面** - 基于Flask的用户友好Web应用
- 📤 **文件上传** - 直接上传Excel文件到浏览器
- 🍽️ **双菜单支持** - 支持A餐和B餐两种菜单类型选择
- 📊 **自动生成PPT** - 从Excel数据自动生成PPT演示文稿
- 💾 **直接下载** - 生成完成后立即下载PPT文件
- ✅ **文件验证** - 智能验证上传的Excel文件有效性
- 🚀 **简化部署** - 支持本地运行和云端部署

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python lunch_app_web.py
```

### 3. 访问应用

在浏览器中打开: `http://127.0.0.1:5000/`

## 📖 使用说明

1. **选择餐类型** - 在页面顶部的下拉菜单中选择 A餐 或 B餐
2. **上传Excel文件** - 点击"选择文件"按钮，上传包含午餐选择数据的Excel文件
3. **生成PPT** - 点击"生成PPT"按钮
4. **下载文件** - 等待处理完成，自动下载生成的PPT文件

## 📋 Excel文件要求

- **格式** - 必须是 `.xlsx` 格式
- **工作表** - 需要包含名称中带有"二4"的工作表
- **数据结构** - 第二行包含日期（B-F列），第三行及以后为学生数据
- **内容** - 需要包含"{菜单类型}餐合计"行（如"A餐合计"、"B餐合计"）

## 🛠️ 技术栈

| 组件 | 说明 |
|------|------|
| **Flask** | Web框架 |
| **pandas** | 数据处理和Excel读取 |
| **openpyxl** | Excel文件操作 |
| **python-pptx** | PPT生成 |
| **Werkzeug** | 文件上传处理 |

## 📁 项目结构

```
lunch-selection-web/
├── lunch_app_web.py      # Flask Web应用主文件
├── fill_ppt.py           # PPT生成核心逻辑
├── application.py        # 生产环境入口（Gunicorn）
├── requirements.txt      # Python依赖
├── runtime.txt          # Python版本配置
├── startup.txt          # 启动命令配置
├── templates/           # PPT模板文件夹
│   └── ppt_temp.pptx    # PPT模板
└── README.md            # 本说明文件
```

## ⚙️ 配置说明

### runtime.txt
指定Python版本（默认为3.9）

### startup.txt
云端部署启动命令（使用Gunicorn）

### requirements.txt
Python依赖包列表

## 🔍 故障排查

| 问题 | 解决方案 |
|------|--------|
| "File is not a zip file" | 确保上传的是有效的.xlsx格式文件 |
| "未找到包含'二4'的sheet" | 检查Excel文件中是否有名称包含"二4"的工作表 |
| 端口被占用 | 修改`lunch_app_web.py`中的端口号 |

## 🌍 部署指南

### 本地部署
```bash
python lunch_app_web.py
```

### 云端部署（Heroku/Render等）
```bash
gunicorn --bind=0.0.0.0 --timeout 600 application:app
```

## 📝 更新日志

### v2.0 - 2026-06-08
- ✨ 添加A/B餐菜单类型选择功能
- ✨ 改进用户界面，文件选择和菜单选择同行显示
- 🐛 增强Excel文件验证机制
- 🔧 改进错误处理和提示信息

### v1.0 - 初始版本
- ✨ 基本的Web界面
- ✨ Excel导入和PPT生成功能

## 📧 联系方式

如有问题或建议，请提交Issue或Pull Request。

## 📄 许可证

MIT License