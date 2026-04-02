from flask import Flask, render_template, request, jsonify
from config import Config
from model_service import model_service
import os
import base64
import time

app = Flask(__name__)

# 允许跨域 (可选，如果前后端分离)
# from flask_cors import CORS
# CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/text/query', methods=['POST'])
def text_query():
    data = request.json
    query = data.get('query', '')
    if not query: return jsonify({"error": "问题为空"}), 400
    
    start = time.time()
    res = model_service.chat(query)
    return jsonify({
        "result": res['response'],
        "source": ",".join(set(res['source'])),
        "confidence": 0.95,
        "duration": f"{time.time()-start:.2f}s"
    })

@app.route('/api/image/analyze', methods=['POST'])
def image_analyze():
    data = request.json
    image_b64 = data.get('image_base64')
    if not image_b64: return jsonify({"error": "无图片"}), 400
    
    try:
        img_data = base64.b64decode(image_b64)
        filename = f"upload_{int(time.time())}.png"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        with open(filepath, 'wb') as f:
            f.write(img_data)
        
        res = model_service.analyze_image(filepath)
        return jsonify({"analysis": res['analysis'], "confidence": res['confidence']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 移除 app.run()，交给 Gunicorn 接管