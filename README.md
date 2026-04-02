# 🏥 MedRAG-Vision: 基于混合检索增强与多模态大模型的智能医疗健康助手

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-blue?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Qwen2.5-LLM-green?style=flat-square&logo=huggingface" alt="Qwen">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker" alt="Docker">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/RAG-检索增强-red?style=flat-square" alt="RAG">
  <img src="https://img.shields.io/badge/多模态-Vision-blue?style=flat-square" alt=" Multimodal">
  <img src="https://img.shields.io/badge/Bootstrap-5-blue?style=flat-square" alt="Bootstrap">
</p>

>  | Linux 生产环境部署版本

## 📌 项目简介

智能医疗健康助手是一个基于**大语言模型 (LLM)** + **多模态模型**的AI医疗问答系统，支持：

- 💬 **文本问答** - 基于RAG检索增强的医疗咨询（症状、用药、健康建议）
- 📷 **医学影像分析** - 基于视觉大模型的X光/CT/皮肤病变图像识别

 📊 日志完整收集

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **RAG 检索增强** | BM25 稀疏检索 + FAISS 稠密检索混合 |
| **多模态支持** | 文本 + 图像双通道输入 |
| **国产大模型** | 基于 Qwen2.5 系列模型 |
| **生产级部署** | Gunicorn + Nginx + Systemd |
| **知识库** | 内置医疗知识库 (medical_knowledge.json) |

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户端                                  │
│   ┌─────────────┐                      ┌─────────────┐          │
│   │  医疗咨询  │                      │  影像分析  │          │
│   │  (文本问答) │                      │  (图片上传) │          │
│   └─────┬─────┘                      └─────┬─────┘          │
└────────┼──────────────────────────────────┼────────────────┘
         │                                  │
         ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Nginx (:80)                                │
│              反向代理 + 静态文件服务                            │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ���                             │
         ▼                             ▼
┌──────────────────┐       ┌──────────────────┐
│   Flask (:5000)   │       │   Qwen2-VL (:5000)│
│   Web 服务        │       │   视觉模型       │
└────────┬─────────┘       └────────┬─────────┘
         │                          GPU
         │                    (图像分析)
         ▼
┌──────────────────────────────────┐
│       RAG Engine                 │
│  ┌──────────┐  ┌──────────────┐ │
│  │  BM25   │  │   FAISS     │ │
│  │(稀疏检索)│  │  (稠密检索) │ │
│  └──────────┘  └──────────────┘ │
└────────┬───────────────────────┘
         │
         ▼
┌──────────────────┐
│  Qwen2.5-文本模型 │
│    (对话生成)     │
└──────────────────┘
```

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | Python 3.10+ / Flask 3.0 / Gunicorn |
| **AI 模型** | Qwen2.5-1.5B-Instruct / Qwen2-VL-2B-Instruct |
| **RAG** | BM25Okapi / FAISS / SentenceTransformers |
| **前端** | HTML5 / CSS3 / JavaScript (原生) |
| **部署** | Nginx / Systemd / Gunicorn |
| **知识库** | JSON 本地存储 |

---

## 🚀 快速开始

### 1. 环境要求

| 要求 | 最低配置 | 推荐配置 |
|------|----------|---------|
| **系统** | Ubuntu 20.04+ | Ubuntu 22.04 LTS |
| **Python** | 3.10 | 3.10~3.12 |
| **GPU** | RTX 3060 6GB | RTX 4090 24GB |
| **显存** | 8GB | 16GB+ |
| **内存** | 16GB | 32GB |
| **磁盘** | 20GB | 50GB SSD |

### 2. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/your-repo/HealthAssistant.git
cd HealthAssistantLinux

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置模型

编辑 `config.py`，根据显存选择模型：

```python
# 方案 A: 显存 > 24GB (如 A100/3090/4090)
TEXT_MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

# 方案 B: 显存 < 16GB (如 T4/3060) - 默认
TEXT_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

# 视觉模型
VISION_MODEL_ID = "Qwen/Qwen2-VL-2B-Instruct"
```

### 4. 启动服务

#### 方式一：开发模式（推荐先测试）

```bash
# 设置环境变量
export CUDA_VISIBLE_DEVICES=0

# 启动 Flask 开发服务器
python app.py
# 访问 http://localhost:5000
```

#### 方式二：生产环境（Gunicorn）

```bash
# 创建日志目录
mkdir -p logs

# 启动 Gunicorn
gunicorn -c gunicorn_conf.py wsgi:app

# 或者后台运行
nohup gunicorn -c gunicorn_conf.py wsgi:app > app.log 2>&1 &
```

#### 方式三：Systemd 守护（推荐）

```bash
# 复制服务文件
sudo cp health_assistant.service /etc/systemd/system/

# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start health-assistant

# 设置开机自启
sudo systemctl enable health-assistant

# 查看状态
sudo systemctl status health-assistant
```

#### 方式四：Nginx 反向代理

```bash
# 复制 Nginx 配置
sudo cp nginx_health.conf /etc/nginx/sites-available/health-assistant

# 创建软链接
sudo ln -s /etc/nginx/sites-available/health-assistant /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 5. 访问系统

```
http://localhost          # 直��访问 (开发模式)
http://localhost:8000   # Gunicorn 端口
http://your_server_ip   # Nginx 反向代理
```



---

## 📁 项目结构

```
HealthAssistantLinux/
├── app.py                 # Flask 应用主入口
├── wsgi.py                # Gunicorn 入口
├── config.py              # 配置文件
├── model_service.py       # 模型服务封装
├── rag_engine.py        # RAG 检索引擎
├── gunicorn_conf.py    # Gunicorn 配置
├── requirements.txt  # Python 依赖
├── nginx_health.conf  # Nginx 配置
├── health_assistant.service  # Systemd 服务
├── 一键部署.sh        # 自动部署脚本
│
├── data/
│   └── medical_knowledge.json  # 医疗知识库
│
├── logs/               # 日志目录
│   ├── access.log
│   └── error.log
│
├── static/
│   └── uploads/        # 用户上传图片
│
└── templates/
    └── index.html     # 前端页面
```

---

## ⚙️ 配置文件说明

### config.py

```python
class Config:
    # === 路径配置 ===
    BASE_DIR = "/home/ubuntu/HealthAssistant"
    UPLOAD_FOLDER = "static/uploads"
    LOG_DIR = "logs"
    
    # === 模型配置 ===
    # 生产环境必须设为 False，使用真实模型
    USE_MOCK = False
    
    # 文本模型 (根据显存选择)
    TEXT_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"  # 或 7B
    VISION_MODEL_ID = "Qwen/Qwen2-VL-2B-Instruct"
    
    # 设备
    DEVICE = "cuda"  # 或 cpu
```

### gunicorn_conf.py

```python
# 核心配置说明
workers = 1        # LLM占用显存大，必须=1
threads = 4         # 多线程处理请求
timeout = 300       # 5分钟超时 (模型推理慢)
keepalive = 5       # 长连接
preload_app = True   # 预加载模型
```

---

## ⚠️ 常见问题

### Q1: 显存不够怎么办？

**解决方案：**
1. 换用小模型 (1.5B)
2. 开启量化 (load_in_4bit=True)
3. 使用 CPU 模式 (USE_MOCK=True 演示)

### Q2: 请求超时 504 怎么办？

**解决方案：**
1. 增加 Nginx 超时时间
2. 增加 Gunicorn timeout
3. 检查模型是否加载成功

### Q3: 如何查看日志？

```bash
# 方式一：Gunicorn 日志
tail -f logs/access.log

# 方式二：Systemd
journalctl -u health-assistant -f

# 方式三：Nginx
tail -f /var/log/nginx/error.log
```

### Q4: 怎么更新知识库？

编辑 `data/medical_knowledge.json`，格式：

```json
[
  {
    "content": "感冒症状描述...",
    "source": "《中国药典》2025版"
  },
  ...
]
```

---

## 📊 模型性能

| 模型 | 参数量 | 显存占用 | 推理速度 |
|------|--------|----------|----------|
| Qwen2.5-1.5B | 1.5B | ~3GB | 快 |
| Qwen2.5-7B | 7B | ~14GB | 中 |
| Qwen2-VL-2B | 2B | ~4GB | 快 |
| Qwen2-VL-7B | 7B | ~14GB | 中 |

---

## 📄 许可证

MIT License

---

## 🎓 关于

- **作者**：齐炜东
- **学校**：太原理工大学
- **���程**：2025年第二次课设
- **指导老师**：XXX

---

## 📚 参考

- [Qwen2.5 模型](https://huggingface.co/Qwen)
- [Flask 文档](https://flask.palletsprojects.com/)
- [Gunicorn 文档](https://docs.gunicorn.org/)
- [RAG 技术详解](https://python.langchain.com/docs/modules/data_connection/)

---

<p align="center">
  <sub>Made with ❤️ for 智能医疗健康助手</sub>
</p>
