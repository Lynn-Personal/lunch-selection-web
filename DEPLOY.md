# 部署指南

## 📋 部署前检查清单

- [x] README.md 已更新
- [x] requirements.txt 已包含所有依赖版本
- [x] .gitignore 已配置
- [x] 所有Python文件已通过语法检查
- [x] 应用已在本地测试通过
- [x] A/B餐功能已验证

## 🚀 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
python lunch_app_web.py

# 3. 访问应用
# 浏览器打开: http://127.0.0.1:5000/
```

## ☁️ 云端部署指南

### Heroku部署

```bash
# 1. 安装Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. 登录Heroku
heroku login

# 3. 创建应用
heroku create your-app-name

# 4. 部署代码
git push heroku main

# 5. 查看应用
heroku open
```

**Procfile内容:**
```
web: gunicorn --bind=0.0.0.0 --timeout 600 application:app
```

### Render部署

```bash
# 1. 连接GitHub仓库到Render
# https://dashboard.render.com

# 2. 创建Web Service
# - Build command: pip install -r requirements.txt
# - Start command: gunicorn --bind=0.0.0.0 --timeout 600 application:app
```

### Railway部署

```bash
# 1. 连接GitHub仓库到Railway
# https://railway.app

# 2. 设置启动命令
# gunicorn --bind=0.0.0.0 --timeout 600 application:app
```

## 🔧 环境变量配置

在云端部署时可设置以下环境变量：

- `FLASK_ENV=production` - 设置为生产环境
- `PORT=8000` - 指定端口（默认5000）

## 📊 性能优化

- 生成PPT时设置了 `--timeout 600`（10分钟超时）
- 使用临时文件处理上传的Excel，避免内存溢出
- 临时文件处理完后自动清理

## 🐛 常见问题

### 1. "template not found"
- 确保 `templates/ppt_temp.pptx` 文件在项目根目录下

### 2. 超时错误
- 调整Gunicorn的`--timeout`参数
- 大文件可能需要更长的处理时间

### 3. 内存不足
- 检查临时文件是否被正确清理
- 考虑增加服务器资源

## 📝 提交到GitHub前

```bash
# 1. 检查git状态
git status

# 2. 添加所有变更
git add .

# 3. 提交更改
git commit -m "整理项目结构，为部署做准备"

# 4. 推送到GitHub
git push origin main
```

## 🔐 安全建议

- 修改Flask的`secret_key`为更强的密钥
- 在生产环境中设置`FLASK_ENV=production`
- 定期更新依赖包版本
- 考虑添加上传文件大小限制

## 📞 问题反馈

如遇到部署问题，请：
1. 检查应用日志
2. 确保所有依赖都已安装
3. 验证环境变量配置
4. 检查文件权限
