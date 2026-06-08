# ☁️ Azure App Service 部署指南（推荐方案）

## 🎯 为什么选择Azure App Service？

| 特性 | Heroku | Render | Azure App Service |
|------|--------|--------|------------------|
| **部署难度** | ⭐ | ⭐ | ⭐ |
| **免费额度** | ❌ | ⚠️ | ✅ **F1免费** |
| **月度成本** | $7+ | 免费/待机 | **$0-15/月** |
| **与MSDN订阅** | ❌ | ❌ | ✅ **包含额度** |
| **自定义域名** | ✅ | ✅ | ✅ |
| **SSL证书** | ✅ | ✅ | ✅ **免费** |
| **Git集成** | ✅ | ✅ | ✅ |

---

## 💰 Azure成本分析

### 免费套餐（F1）
```
✅ 完全免费，无需信用卡
✅ 1GB RAM + 10GB存储
✅ 每天可用时间充足
✅ 自动扩展（低流量时休眠）
✅ 适合开发/测试/中小型应用

限制：
• 无法自定义域名（只能用*.azurewebsites.net）
• 共享基础设施
• 内存和CPU有限
```

### B1基础版（推荐）
```
💰 约 ¥90/月（西欧数据中心）
    约 ¥150/月（美国东部）
    
✅ 专用基础设施
✅ 支持自定义域名
✅ 更好的性能
✅ 24/7监控

中国MSDN订阅通常赠送：
• ￥150/月的Azure额度
• 足够支付B1基础版！
```

---

## 🚀 快速部署步骤（10分钟）

### 前提准备
```
✅ Azure订阅（你已有）
✅ GitHub账户
✅ lunch-selection-web项目
```

### 步骤1：登录Azure门户

```
访问: https://portal.azure.com
使用Microsoft账号登录
```

### 步骤2：创建资源组

```
1. 首页 → 创建资源
2. 搜索 "资源组"
3. 创建新资源组：
   - 名称: lunch-app-rg
   - 区域: 东亚 (或其他靠近用户的地区)
4. 点击 "创建"
```

### 步骤3：创建App Service

```
1. 首页 → 创建资源
2. 搜索 "App Service"
3. 点击 "创建"
4. 填写基本信息：

   应用名称: lunch-selection-app
   (最终URL: https://lunch-selection-app.azurewebsites.net/)
   
   发布: 代码
   
   运行时堆栈: Python 3.9
   
   操作系统: Linux
   
   区域: 东亚（中国内地最快）
      或 东南亚（新加坡）
   
   定价计划:
   ├─ 免费 (F1) - $0/月
   └─ 基础 (B1) - ~¥90/月 ✅ 推荐

5. 点击 "审阅 + 创建"
6. 点击 "创建"（等待2-3分钟）
```

### 步骤4：配置部署源

```
1. 创建完成后 → "转到资源"

2. 左侧菜单 → "部署中心"

3. 选择 "GitHub"
   ├─ 点击 "授权" → 登录GitHub
   └─ 同意权限请求

4. 选择：
   - 组织: Lynn-Personal
   - 仓库: lunch-selection-web
   - 分支: master

5. 点击 "保存"
   (首次部署需要2-3分钟)
```

### 步骤5：验证部署

```
1. 部署完成后，访问应用：
   https://lunch-selection-app.azurewebsites.net/

2. 如果看到午餐选择PPT生成器界面 ✅
   部署成功！

3. 左侧菜单 → "概览" 
   查看应用状态和日志
```

### 完成！🎉
```
你的应用已在线！

URL: https://lunch-selection-app.azurewebsites.net/

所有人可以访问这个链接！
```

---

## 🔧 必需的配置

### 1. 配置Python启动命令

```
1. 左侧菜单 → "配置"

2. 常规设置 → 启动命令：
   gunicorn --bind=0.0.0.0 --timeout 600 application:app

3. 点击 "保存"
```

### 2. 配置应用设置

```
1. 左侧菜单 → "配置"

2. 应用设置 → 新增：

名称: FLASK_ENV
值: production

---

名称: SCM_DO_BUILD_DURING_DEPLOYMENT
值: true

---

名称: PORT
值: 8000

3. 点击 "保存"
```

### 3. 配置Python版本

```
1. 左侧菜单 → "配置"

2. 常规设置 → Python版本：
   3.9 (或更高)

3. 点击 "保存"
```

---

## 📊 项目结构验证

确保你的GitHub仓库中有：

```
✅ requirements.txt        # 依赖列表
✅ application.py          # Gunicorn入口
✅ lunch_app_web.py        # Flask应用
✅ fill_ppt.py             # 核心逻辑
✅ templates/ppt_temp.pptx # PPT模板
✅ .gitignore              # 忽略文件
✅ Procfile (可选)         # 启动配置
```

---

## 🌍 配置自定义域名（可选）

仅限于B1基础版或更高

### 步骤1：购买域名

选择以下任一：
- 阿里云: aliyun.com
- 腾讯云: cloud.tencent.com
- Namecheap: namecheap.com
- Godaddy: godaddy.com

### 步骤2：在Azure中添加

```
1. 左侧菜单 → "自定义域"

2. 点击 "+ 添加自定义域"

3. 输入你的域名：
   lunch-app.com

4. 复制提供的TXT记录

5. 在域名注册商中添加DNS记录：
   - 类型: CNAME (或A记录)
   - 值: lunch-selection-app.azurewebsites.net

6. 点击 "添加"

7. 配置HTTPS（SSL）：
   - 点击 "添加绑定"
   - 自动生成免费证书
```

---

## 📈 监控和调试

### 查看日志

```
1. 左侧菜单 → "日志流"
2. 实时查看应用日志
3. 帮助排查问题
```

### 性能指标

```
1. 左侧菜单 → "指标"
2. 查看：
   - CPU使用率
   - 内存使用
   - 请求数
   - 响应时间
```

### 诊断和解决问题

```
1. 左侧菜单 → "诊断和解决问题"
2. 查看常见问题
3. 应用重启/停止
```

---

## 🚀 自动更新部署

### 优势
只需将改动push到GitHub，Azure会自动部署！

### 流程
```
本地修改代码
    ↓
git commit -m "message"
    ↓
git push origin master
    ↓
GitHub webhook触发
    ↓
Azure自动部署
    ↓
应用自动更新（2-3分钟）
```

### 查看部署历史

```
1. 左侧菜单 → "部署中心"
2. 查看所有部署记录
3. 查看构建日志
```

---

## ⚙️ 高级配置

### 1. 环境变量

```
左侧菜单 → 配置 → 应用设置

添加任何需要的环境变量：

SECRET_KEY=your-very-secret-key
MAX_UPLOAD_SIZE=52428800
MAINTENANCE_MODE=false
```

### 2. 连接字符串

如果要添加数据库：

```
左侧菜单 → 配置 → 连接字符串

示例（Azure SQL Database）：
名称: DefaultConnection
值: Server=...;User ID=...;Password=...
选择: SQLAzure
```

### 3. 备份设置

```
左侧菜单 → 备份

定期备份你的应用
```

---

## 📱 多机器访问

所有学生只需：

```
1. 打开浏览器
2. 输入URL或扫描二维码
3. 访问应用

URL: https://lunch-selection-app.azurewebsites.net/

或自定义域名: https://lunch-app.com/
```

### 推荐方式

```
方式1（最简单）：
在班级群里分享URL
所有人直接点击打开

方式2（更专业）：
购买域名后分享
更容易记住

方式3（体验感强）：
生成二维码投屏
学生扫描访问
```

---

## 💡 成本总结

### 使用MSDN/Azure订阅

```
❌ 如果选择F1（免费）
   月成本: ¥0 × 无限使用 = ¥0

✅ 如果选择B1（推荐）
   月成本: ¥90 左右
   MSDN额度: 通常 ¥150/月
   
结果: 
   实际成本 = ¥0（额度足够覆盖）
   每月还剩¥60额度用于其他Azure服务
```

### vs Heroku/Render

```
Heroku:  $7/月 × 12 = $84/年
Render:  $0-7/月（取决于选择）
Azure:   ¥0/月（用MSDN额度）

Azure节省最多！
```

---

## 🔐 安全最佳实践

### 1. 修改Secret Key

修改 `application.py` 中的:

```python
app.secret_key = 'change-this-to-a-secure-random-key'
```

改为强密钥，然后push到GitHub

### 2. 启用HTTPS

```
左侧菜单 → TLS/SSL设置
启用 "仅HTTPS"
```

### 3. 访问限制（可选）

```
左侧菜单 → 网络
配置：
- 防火墙规则
- IP白名单
```

---

## 🆚 Azure vs 其他方案对比

```
┌─────────────────────────────────────────┐
│   Azure App Service (推荐用你的订阅)    │
├─────────────────────────────────────────┤
│ ✅ 成本: ¥0/月（用MSDN额度）            │
│ ✅ 难度: ⭐ 极简单                      │
│ ✅ 部署: git push自动部署               │
│ ✅ 监控: 完整的仪表板                   │
│ ✅ 域名: 支持自定义域名                 │
│ ✅ SSL: 免费HTTPS证书                  │
│ ✅ Microsoft技术支持                    │
│ ✅ 中国区域可用（东亚机房）             │
│ ❌ 免费版有性能限制                     │
└─────────────────────────────────────────┘
```

---

## 📋 检查清单

部署前：
- [ ] Azure订阅已登录
- [ ] GitHub项目已提交
- [ ] requirements.txt完整
- [ ] application.py存在
- [ ] Procfile已配置

部署中：
- [ ] App Service已创建
- [ ] Python运行时已设置
- [ ] GitHub已授权
- [ ] 自动部署已启用

部署后：
- [ ] 访问URL成功
- [ ] 上传文件功能正常
- [ ] PPT生成成功
- [ ] 日志无错误

---

## 🆘 常见问题

### Q: 应用显示500错误

A: 
```
1. 检查左侧菜单 → "日志流"
2. 查看详细错误信息
3. 检查应用设置中的变量
4. 重启应用
```

### Q: 上传文件失败

A:
```
1. 检查文件大小（默认50MB）
2. 验证模板文件是否存在
3. 查看日志中的错误信息
4. 修改配置中的 MAX_CONTENT_LENGTH
```

### Q: 访问速度慢

A:
```
1. 如果使用F1免费版 → 升级到B1
2. 应用在闲置时会休眠
3. 访问时会重新启动（2-3秒）
```

### Q: 部署失败

A:
```
1. 检查GitHub授权是否成功
2. 查看部署日志
3. 确保分支是master
4. 检查requirements.txt格式
```

---

## 🚀 快速开始命令

如果已有Azure CLI：

```bash
# 1. 登录
az login

# 2. 创建资源组
az group create \
  --name lunch-app-rg \
  --location eastasia

# 3. 创建App Service计划
az appservice plan create \
  --name lunch-app-plan \
  --resource-group lunch-app-rg \
  --sku F1 \
  --is-linux

# 4. 创建Web应用
az webapp create \
  --resource-group lunch-app-rg \
  --plan lunch-app-plan \
  --name lunch-selection-app \
  --runtime "PYTHON|3.9"

# 5. 配置GitHub部署
az webapp deployment source config-zip \
  --resource-group lunch-app-rg \
  --name lunch-selection-app \
  --src lunch-selection-web.zip
```

---

## 📞 获取帮助

### Azure文档
- [官方文档](https://docs.microsoft.com/azure)
- [Python开发指南](https://docs.microsoft.com/python)
- [故障排查](https://docs.microsoft.com/azure/app-service/troubleshoot-common-app-service-errors)

### 技术支持
- Azure门户内的帮助 → "帮助 + 支持"
- Microsoft Q&A 社区
- Stack Overflow标签: azure-app-service

---

## ✅ 最终步骤

1. **现在就做** (10分钟)
   ```
   登录 https://portal.azure.com
   创建App Service
   配置Git部署
   ```

2. **立即上线** (2-3分钟)
   ```
   首次部署完成
   获得URL
   分享给所有人
   ```

3. **享受无忧** (永久)
   ```
   无需维护
   自动更新
   免费使用
   ```

---

## 🎉 成功标志

✅ 部署完成后，你将看到：

```
✅ 应用状态: 运行中
✅ URL: https://lunch-selection-app.azurewebsites.net/
✅ 可以上传文件
✅ 可以生成PPT
✅ 可以下载文件
✅ 所有人都能访问
```

**现在你的应用已经是真正的云端应用了！** 🚀

---

## 🔗 需要帮助？

有任何问题，可以：
1. 查看Azure门户中的"诊断和解决问题"
2. 查看"日志流"中的实时错误
3. 访问Azure官方文档
4. 检查GitHub部署状态

**最后，祝部署成功！** 🎊
