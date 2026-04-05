from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import requests
import shutil
import json
import os

# 尝试加载 .env 文件（本地开发用）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # 如果没有 python-dotenv，直接用系统环境变量

# 从环境变量读取 API Key（安全做法，不写死在代码里）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("❌ 请设置环境变量 DEEPSEEK_API_KEY，或在 .env 文件中配置")

def ask_deepseek(user_text: str) -> str:
    """调用 DeepSeek API"""
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",  # 或者 "deepseek-reasoner"（推理模型，慢但强）
            "messages": [
                {"role": "system", "content": "你是一个有帮助的语音助手，回答要简洁自然，适合语音播报。"},
                {"role": "user", "content": user_text}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        res = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        result = res.json()
        return result["choices"][0]["message"]["content"]
        
    except Exception as e:
        return f"AI 思考出错了：{str(e)}"





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 自动查找 ffmpeg 路径
FFMPEG_PATH = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"

# 百度语音 API 配置（请替换为你自己的真实密钥）
BAIDU_APP_ID = "7602428"
# 从环境变量读取百度 API Key
BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")
if not BAIDU_API_KEY or not BAIDU_SECRET_KEY:
    raise ValueError("❌ 请设置环境变量 BAIDU_API_KEY 和 BAIDU_SECRET_KEY，或在 .env 文件中配置")


def get_baidu_token():
    """获取百度 API 访问令牌"""
    try:
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_API_KEY}&client_secret={BAIDU_SECRET_KEY}"
        res = requests.post(url, timeout=10)
        result = res.json()
        token = result.get("access_token")
        if not token:
            print(f"获取百度 token 失败: {result}")
        return token
    except Exception as e:
        print(f"获取百度 token 异常: {e}")
        return None


async def text_to_speech_internal(text: str) -> dict:
    """内部函数：文字转语音（供 upload_audio 调用）"""
    try:
        token = get_baidu_token()
        if not token:
            return None
        
        url = f"https://tsn.baidu.com/text2audio?tex={text}&tok={token}&cuid=123456&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=0"
        
        res = requests.post(url, timeout=10)
        
        # 检查返回的是不是音频（MP3 头: ID3 或 帧同步字）
        if res.headers.get('Content-Type') == 'audio/mp3' or res.content[:3] == b'ID3' or res.content[:2] == b'\xff\xfb':
            # 保存音频文件
            audio_path = os.path.join(UPLOAD_DIR, f"tts_{hash(text)}.mp3")
            with open(audio_path, "wb") as f:
                f.write(res.content)
            print(f"✅ TTS 生成成功: {audio_path}")
            return {"audio_url": f"/audio/{os.path.basename(audio_path)}"}
        else:
            print(f"❌ TTS 生成失败: {res.text}")
            return None
            
    except Exception as e:
        print(f"❌ TTS 异常: {e}")
        return None


@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """接收前端上传的音频文件并进行语音识别"""
    print(f"📁 收到文件上传: {file.filename}, content_type: {file.content_type}")
    
    # 统一使用 .webm 扩展名
    filepath = os.path.join(UPLOAD_DIR, "voice.webm")
    
    try:
        # 保存上传的文件
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)
        print(f"✅ 文件已保存: {filepath}, 大小: {len(content)} bytes")
        
        # 检查文件头是否有效
        with open(filepath, "rb") as f:
            header = f.read(4)
            # WebM/Matroska 文件头: 1A 45 DF A3
            if header != b'\x1aE\xdf\xa3':
                print(f"⚠️ 警告: 文件头无效: {header.hex()}, 期望: 1a45dfa3")
                # 尝试用文件内容类型检测
                if len(content) < 100:
                    return {"error": "音频文件太小或无效"}
        
        # 检查 ffmpeg 是否可用
        if not shutil.which("ffmpeg"):
            print("⚠️ 警告: ffmpeg 未安装，无法转换音频格式")
            return {"error": "服务器未配置音频转换工具 (ffmpeg)"}
        
        # 转成 wav（百度 ASR 需要）
        wav_path = filepath.replace('.webm', '.wav')
        
        # 使用 subprocess 调用 ffmpeg（更稳定）
        cmd = [
            FFMPEG_PATH,
            "-i", filepath,
            "-ar", "16000",
            "-ac", "1", 
            "-acodec", "pcm_s16le",
            "-y",
            wav_path
        ]
        
        print(f"🔄 转换音频格式: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ 音频转换失败: {result.stderr}")
            return {"error": f"音频转换失败: {result.stderr}"}
        
        print(f"✅ 音频已转换为 WAV: {wav_path}")
        
        # 调用百度 ASR
        token = get_baidu_token()
        if not token:
            return {"error": "无法获取百度语音识别服务令牌，请检查 API 密钥配置"}
        
        url = f"https://vop.baidu.com/server_api?dev_pid=1537&cuid=123456&token={token}"
        
        with open(wav_path, "rb") as f:
            audio_data = f.read()
        
        print(f"📤 发送语音识别请求，数据大小: {len(audio_data)} bytes")
        
        headers = {"Content-Type": "audio/pcm;rate=16000"}
        res = requests.post(url, data=audio_data, headers=headers, timeout=30)
        result = res.json()
        
        print(f"📥 百度 API 响应: {result}")
        
        if result.get("err_no") == 0:
            recognized_text = result["result"][0] if result["result"] else ""
            print(f"✅ 识别成功: {recognized_text}")
            
            # 调用 DeepSeek 生成回复
            ai_reply = ask_deepseek(recognized_text)
            print(f"🤖 AI 回复: {ai_reply}")
            
            # 生成 TTS（把 AI 回复转成语音）
            tts_result = await text_to_speech_internal(ai_reply)
            
            return {
                "text": recognized_text,      # 识别的文字
                "reply": ai_reply,             # AI 的回复
                "audio_url": tts_result.get("audio_url") if tts_result else None
            }
        else:
            error_msg = result.get("err_msg", "识别失败")
            print(f"❌ 识别失败: {error_msg}")
            return {"error": f"语音识别失败: {error_msg}"}
            
    except Exception as e:
        print(f"❌ 处理异常: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"服务器处理错误: {str(e)}"}


@app.get("/")
def health():
    return {"status": "Day2 Voice Assistant Ready", "version": "1.2"}


@app.post("/tts")
async def text_to_speech(text: str):
    """文字转语音"""
    try:
        token = get_baidu_token()  # 复用之前的函数
        
        # 百度 TTS 接口
        url = f"https://tsn.baidu.com/text2audio?tex={text}&tok={token}&cuid=123456&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=0&aue=3"
        
        # aue=3 返回 mp3 格式
        
        res = requests.get(url, timeout=10)
        
        if res.headers.get("Content-Type") == "audio/mp3":
            # 保存音频文件
            audio_path = f"uploads/tts_{hash(text)}.mp3"
            with open(audio_path, "wb") as f:
                f.write(res.content)
            
            return {"status": "ok", "audio_url": f"/uploads/{os.path.basename(audio_path)}"}
        else:
            return {"error": "TTS 生成失败"}
            
    except Exception as e:
        return {"error": str(e)}


from fastapi.responses import FileResponse

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """提供 TTS 生成的音频文件"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mp3")
    return {"error": "文件不存在"}
