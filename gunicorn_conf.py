import multiprocessing

# 绑定地址 (内网)
bind = "0.0.0.0:8000"

# === 核心并发策略 ===
#由于 LLM 占用显存极大，不能开启多个 worker (每个 worker 都会加载一份模型)
# 除非你有 4 张显卡，否则 workers 必须设为 1
workers = 1

# 使用多线程处理 Web 请求，避免 I/O 阻塞
threads = 4 

# === 超时设置 ===
# 模型推理可能需要较长时间，必须设置超长超时，否则会被 kill
timeout = 300  # 5分钟超时
keepalive = 5

# === 日志 ===
accesslog = "/home/ubuntu/HealthAssistant/logs/access.log"
errorlog =  "/home/ubuntu/HealthAssistant/logs/error.log"
loglevel = "info"

# === 预加载 ===
# True: 在启动 worker 前加载 app 代码 (节省内存，但初始化慢)
preload_app = True