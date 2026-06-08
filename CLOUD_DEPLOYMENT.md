# ☁️ 云端部署完全指南

## 📊 部署方案对比

| 方案 | 价格 | 难度 | 性能 | 推荐指数 | 描述 |
|------|------|------|------|--------|------|
| **Heroku** | 付费 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 最简单，集成git push自动部署 |
| **Render** | 免费/付费 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Heroku替代品，免费套餐可用 |
| **Railway** | 免费/付费 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 友好的界面，免费额度充足 |
| **Azure App Service** | 付费 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 企业级，功能完整 |
| **AWS EC2** | 付费 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 需要配置，功能最强大 |
| **Docker + VPS** | 付费 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 完全控制，成本可控 |

---

## 🚀 推荐方案 1：Heroku（最简单，付费）

### ✅ 优势
- 一键部署：`git push heroku main`
- 自动SSL/HTTPS
- 内置监控和日志
- 全球CDN加速

### 📋 部署步骤

```bash
# 1. 安装Heroku CLI
# Windows: 下载 https://devcenter.heroku.com/articles/heroku-cli

# 2. 登录账户
heroku login

# 3. 创建应用
heroku create lunch-selection-app

# 4. 部署
git push heroku main

# 5. 查看日志
heroku logs --tail

# 6. 打开应用
heroku open
```

### 💰 成本
- **免费层**：已停用（2022年）
- **标准版**：$7/月（1个Web Dyno）
- **性能版**：$50+/月

### 🔗 访问链接
```
https://lunch-selection-app.herokuapp.com/
```

---

## 🚀 推荐方案 2：Render（最佳平衡，免费+付费）

### ✅ 优势
- 免费套餐可用（受限）
- 自动Git集成
- 无需信用卡即可免费试用
- 简洁的仪表板

### 📋 部署步骤

```bash
# 1. 访问 https://render.com

# 2. 用GitHub账号登录

# 3. 创建New Web Service
# - 选择GitHub仓库: lunch-selection-web
# - Build command: pip install -r requirements.txt
# - Start command: gunicorn --bind=0.0.0.0 --timeout 600 application:app

# 4. 部署完成后获得URL
# https://lunch-selection-app.onrender.com/
```

### 💰 成本
- **免费层**：限制（自动休眠）
- **Pro**：$7/月
- **Premium**：$25+/月

### 🌟 推荐理由
最适合中小型项目！

---

## 🚀 推荐方案 3：Railway（用户友好，付费）

### ✅ 优势
- $5/月起价
- 无需休眠
- 简单的配置界面
- 支持多种语言和框架

### 📋 部署步骤

```bash
# 1. 访问 https://railway.app

# 2. 用GitHub登录

# 3. 创建New Project
# - 选择Deploy from GitHub

# 4. 自动部署
# 系统自动检测python并部署

# 5. 获得URL
# https://your-project.railway.app/
```

### 💰 成本
- 按使用量计费，起价$5/月

---

## 🐳 高级方案：Docker + 自建服务器

### ✅ 优势
- 完全控制
- 成本可控（VPS $5-20/月）
- 可扩展性强
- 学习价值高

### 📋 部署步骤

#### 1. 创建Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PORT=5000

CMD ["gunicorn", "--bind=0.0.0.0", "--timeout=600", "--workers=4", "application:app"]
```

#### 2. 创建docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:5000"
      - "443:5000"
    environment:
      - FLASK_ENV=production
      - PORT=5000
    restart: always
    volumes:
      - ./templates:/app/templates
```

#### 3. 部署到VPS

```bash
# 1. 连接到VPS
ssh root@your_server_ip

# 2. 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. 克隆项目
git clone https://github.com/Lynn-Personal/lunch-selection-web.git
cd lunch-selection-web/lunch-selection-web

# 4. 构建镜像
docker build -t lunch-app .

# 5. 运行容器
docker-compose up -d

# 6. 查看日志
docker-compose logs -f
```

#### 4. 配置Nginx反向代理

```nginx
# /etc/nginx/sites-available/lunch-app
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 启用配置
sudo ln -s /etc/nginx/sites-available/lunch-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. 配置SSL证书（Let's Encrypt）

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 🌐 多区域部署架构

### 架构图

```
┌─────────────────────────────────────┐
│      用户访问 (全球)                 │
└─────────┬───────────────────────────┘
          │
┌─────────▼───────────────────────────┐
│   CloudFlare CDN (缓存加速)          │
└─────────┬───────────────────────────┘
          │
┌─────────▼───────────────────────────┐
│   负载均衡器 (负载分散)              │
└───┬─────────────────────────┬───────┘
    │                         │
┌───▼──────────┐      ┌──────▼────────┐
│ 应用服务器1  │      │ 应用服务器2   │
│ (区域1)      │      │ (区域2)       │
└───┬──────────┘      └──────┬────────┘
    │                        │
┌───▼────────────────────────▼────────┐
│   数据存储 (共享)/缓存 (Redis)       │
└─────────────────────────────────────┘
```

---

## 📈 扩展方案

### 方案A：简单扩展（推荐初期）

```bash
# 单个实例，自动重启
# Render或Railway上直接操作
# - 增加实例数量
# - 提升实例规格
```

### 方案B：Kubernetes扩展（高级）

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lunch-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lunch-app
  template:
    metadata:
      labels:
        app: lunch-app
    spec:
      containers:
      - name: lunch-app
        image: your-registry/lunch-app:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

## 🔐 安全部署建议

### 1. 环境变量配置

```bash
# .env (本地)
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-change-this
MAX_UPLOAD_SIZE=52428800  # 50MB
```

### 2. 在云平台设置环境变量

**Heroku示例：**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secure-key
```

**Render示例：**
在仪表板 → Environment 中添加

### 3. 上传文件大小限制

修改 `lunch_app_web.py`：

```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB限制

@app.before_request
def limit_upload_size():
    if request.content_length and request.content_length > app.config['MAX_CONTENT_LENGTH']:
        abort(413, "File too large")
```

### 4. 速率限制

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def upload_file():
    # 防止滥用
    pass
```

---

## 📊 监控和日志

### Heroku监控

```bash
# 实时日志
heroku logs --tail

# 性能指标
heroku metrics

# 错误追踪
heroku logs -p web
```

### 使用第三方监控

1. **Sentry** - 错误追踪
2. **New Relic** - 性能监控
3. **Datadog** - 全面监控
4. **LogRocket** - 会话录制

---

## 💾 持久化存储

如果需要保存生成的PPT：

### 选项1：AWS S3（推荐）

```python
import boto3

s3_client = boto3.client('s3')

def upload_to_s3(file_path, bucket_name):
    s3_client.upload_file(
        file_path,
        bucket_name,
        f"ppt/{os.path.basename(file_path)}"
    )
```

### 选项2：Azure Blob Storage

```python
from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient.from_connection_string(
    "your_connection_string"
)
```

### 选项3：Google Cloud Storage

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('your-bucket')
```

---

## 🎯 完整部署流程总结

### 最快方案（15分钟）：Render

```bash
# 1. Fork项目到你的GitHub
# 2. 访问 render.com
# 3. 连接GitHub账户
# 4. 选择lunch-selection-web项目
# 5. 一键部署完成！
# 6. 获得URL: https://your-app.onrender.com
```

### 最经济方案（$5-10/月）：Railway或Render Pro

```bash
# 类似Render流程
# 成本 $7/月起
```

### 企业方案（需要更多控制）：Docker + VPS

```bash
# VPS成本: $5-20/月
# 完全控制，学习资源多
```

---

## 🔗 获得访问链接的方式

### 1. 获得固定域名

**购买域名：**
- Namecheap: $0.88/年
- Godaddy: $1.99/年
- 阿里云: ¥55/年

**指向云平台：**

例如Render：
```
DNS CNAME record:
your-app.onrender.com
```

### 2. 使用免费子域名

- Vercel: `*.vercel.app`
- Netlify: `*.netlify.app`
- Render: `*.onrender.com`
- Railway: `*.railway.app`

### 3. 共享方式

所有机器可通过以下方式访问：

```
https://your-app.onrender.com/
https://your-custom-domain.com/
```

只需告知URL即可，无需额外配置！

---

## 🚨 部署前检查清单

- [ ] 所有代码已提交到GitHub
- [ ] requirements.txt包含所有依赖
- [ ] Procfile或deployment文件已准备
- [ ] 环境变量已列出
- [ ] 敏感信息已从代码中移除
- [ ] 测试了本地运行
- [ ] README包含使用说明

---

## 📞 快速决策树

```
是否需要免费试用？
├─ 是 → 选择 Render (免费层)
└─ 否 → 对比成本和功能

是否需要最简单部署？
├─ 是 → 选择 Heroku 或 Render
└─ 否 → 可考虑Docker/Kubernetes

是否需要完全控制？
├─ 是 → Docker + VPS
└─ 否 → PaaS (Heroku/Render/Railway)

是否需要全球加速？
└─ 是 → 添加CloudFlare或Cloudfront
```

---

## 📚 相关资源

- [Heroku官方文档](https://devcenter.heroku.com/)
- [Render部署指南](https://render.com/docs)
- [Railway文档](https://docs.railway.app/)
- [Docker官方教程](https://docs.docker.com/)
- [Flask部署最佳实践](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 🎉 推荐方案

**对于你的项目，推荐：**

1. **现在** → Render免费层体验
2. **小规模使用** → Railway ($5/月)
3. **商用/高流量** → Heroku或自建Docker
4. **企业级** → Azure或AWS

任选其一，都能实现：
✅ 24/7运行
✅ 多机器访问
✅ 固定URL分享
✅ 自动重启保障
