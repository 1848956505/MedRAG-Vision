import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor, Qwen2VLForConditionalGeneration
from PIL import Image
from config import Config
from rag_engine import rag_engine


class HealthModelService:
    def __init__(self):
        self.mock = Config.USE_MOCK
        if not self.mock:
            print("正在加载模型，请稍候（首次运行需下载模型）...")
            # 加载文本模型
            self.text_tokenizer = AutoTokenizer.from_pretrained(Config.TEXT_MODEL_ID, trust_remote_code=True)
            self.text_model = AutoModelForCausalLM.from_pretrained(
                Config.TEXT_MODEL_ID,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True
            )

            # 加载视觉模型
            self.vl_processor = AutoProcessor.from_pretrained(Config.VISION_MODEL_ID, trust_remote_code=True)
            self.vl_model = Qwen2VLForConditionalGeneration.from_pretrained(
                Config.VISION_MODEL_ID,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True
            )
            print("模型加载完成！")

    def chat(self, query):
        # 1. 检索增强 (RAG)
        retrieved = rag_engine.search(query)
        context = "\n".join([f"- {item['content']} (来源: {item['source']})" for item in retrieved])

        # 2. 构建 Prompt
        prompt = f"""你是一个专业的健康助手。请基于以下参考信息回答用户问题。如果参考信息不足，请基于你的专业知识回答，但需注明仅供参考。

        【参考信息】：
        {context}

        【用户问题】：{query}
        """

        # 3. 推理 (或 Mock)
        if self.mock:
            return {
                "response": f"[模拟回答] 针对您的问题“{query}”，建议如下：\n根据《中国药典》2025版参考信息：{retrieved[0]['content']}\n请注意：这只是模拟系统的回复，非真实医疗建议。",
                "source": [r['source'] for r in retrieved]
            }
        else:
            messages = [{"role": "user", "content": prompt}]
            text = self.text_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            model_inputs = self.text_tokenizer([text], return_tensors="pt").to(Config.DEVICE)

            generated_ids = self.text_model.generate(**model_inputs, max_new_tokens=512)
            response = self.text_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

            # 简单的后处理，去除Prompt部分
            response_clean = response.split("assistant")[-1].strip()
            return {"response": response_clean, "source": [r['source'] for r in retrieved]}

    def analyze_image(self, image_path):
        if self.mock:
            return {
                "analysis": "检测到胸部影像特征。左下肺野纹理增粗，未见明显结节影。[这是模拟的分析结果]",
                "confidence": 0.92
            }
        else:
            # Qwen2-VL 推理逻辑
            image = Image.open(image_path)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": "请从医学角度详细分析这张图片，指出可能的异常特征。"}
                    ],
                }
            ]
            text = self.vl_processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.vl_processor(text=[text], images=[image], return_tensors="pt", padding=True).to(Config.DEVICE)

            generated_ids = self.vl_model.generate(**inputs, max_new_tokens=512)
            response = self.vl_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return {"analysis": response, "confidence": 0.85}


# 单例模式
model_service = HealthModelService()