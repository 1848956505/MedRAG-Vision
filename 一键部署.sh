# 1. 更新系统并安装基础库
sudo apt update
sudo apt install -y python3-pip python3-venv nginx git

# 2. 创建项目目录 (假设上传了代码到这里)
cd /home/ubuntu/HealthAssistant

# 3. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 4. 安装 Python 依赖
# 必须安装 gunicorn，且推荐安装 hf_transfer 加速模型下载
pip install --upgrade pip
pip install gunicorn hf_transfer
pip install -r requirements.txt

# 5. 配置 Systemd 服务
# 将上面的 health_assistant.service 内容复制到文件
sudo nano /etc/systemd/system/health_assistant.service
# (粘贴内容后 Ctrl+O 保存, Ctrl+X 退出)

# 6. 启动服务
sudo systemctl daemon-reload
sudo systemctl start health_assistant
sudo systemctl enable health_assistant

# 7. 查看服务状态 (非常重要，看日志用)
sudo systemctl status health_assistant
# 如果报错，查看详细日志：
# journalctl -u health_assistant -f

# 8. 配置 Nginx
sudo nano /etc/nginx/sites-available/health_assistant
# (粘贴 nginx_health.conf 内容)

# 建立软链接生效
sudo ln -s /etc/nginx/sites-available/health_assistant /etc/nginx/sites-enabled/
# 测试配置并重启 Nginx
sudo nginx -t
sudo systemctl restart nginx

# 9. 防火墙设置 (如果开启了 ufw)
sudo ufw allow 'Nginx Full'