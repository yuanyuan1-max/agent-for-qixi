"""
Web应用界面
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

from agents.dating_agent import DatingAgent
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="七夕约会指南RAG智能体",
    description="基于LLaMA和LangChain的智能约会规划系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class DatingRequest(BaseModel):
    query: str
    user_preferences: Optional[Dict[str, Any]] = None

# 响应模型
class DatingResponse(BaseModel):
    answer: str
    source_documents: List[Dict[str, Any]]
    search_results: List[Dict[str, Any]]
    status: str

# 全局智能体实例
dating_agent = None

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    global dating_agent
    try:
        logger.info("正在初始化约会指南智能体...")
        dating_agent = DatingAgent()
        logger.info("智能体初始化完成")
    except Exception as e:
        logger.error(f"智能体初始化失败: {e}")
        dating_agent = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径，返回HTML界面"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>七夕约会指南RAG智能体</title>
        <style>
            body { font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
            .header { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 30px; text-align: center; }
            .header h1 { margin: 0; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .content { padding: 30px; }
            .input-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; }
            textarea { width: 100%; padding: 15px; border: 2px solid #e1e5e9; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
            button { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 16px; cursor: pointer; font-weight: bold; }
            .result-section { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #ff6b6b; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💕 七夕约会指南</h1>
                <p>基于AI的智能约会规划系统</p>
            </div>
            
            <div class="content">
                <div class="input-group">
                    <label for="query">请描述你的约会需求：</label>
                    <textarea id="query" rows="4" placeholder="例如：我想在七夕节为女朋友准备一个浪漫的约会，预算1000元以内，她喜欢看电影和美食..."></textarea>
                </div>
                
                <button onclick="planDating()">🎯 开始规划约会</button>
                
                <div id="resultSection" style="display: none;">
                    <div class="result-section">
                        <h3>💡 约会规划建议</h3>
                        <div id="datingPlan"></div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function planDating() {
                const query = document.getElementById('query').value.trim();
                if (!query) { alert('请输入你的约会需求'); return; }
                
                try {
                    const response = await fetch('/api/plan-dating', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query, user_preferences: {}})
                    });
                    
                    if (!response.ok) throw new Error('请求失败');
                    
                    const result = await response.json();
                    document.getElementById('datingPlan').innerHTML = result.answer.replace(/\\n/g, '<br>');
                    document.getElementById('resultSection').style.display = 'block';
                    
                } catch (error) {
                    console.error('Error:', error);
                    document.getElementById('datingPlan').innerHTML = '<p style="color: red;">抱歉，规划约会时出现错误，请稍后重试。</p>';
                    document.getElementById('resultSection').style.display = 'block';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/plan-dating", response_model=DatingResponse)
async def plan_dating(request: DatingRequest):
    """规划约会API"""
    try:
        if not dating_agent:
            raise HTTPException(status_code=503, detail="智能体未初始化")
        
        logger.info(f"收到约会规划请求: {request.query}")
        
        # 调用智能体规划约会
        result = dating_agent.plan_dating(request.query)
        
        return DatingResponse(
            answer=result["answer"],
            source_documents=result["source_documents"],
            search_results=result["search_results"],
            status="success"
        )
        
    except Exception as e:
        logger.error(f"规划约会失败: {e}")
        raise HTTPException(status_code=500, detail=f"规划约会失败: {str(e)}")

@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    try:
        if not dating_agent:
            return {"status": "not_initialized"}
        
        status = dating_agent.get_agent_status()
        return {"status": "ready", "details": status}
        
    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("web.app:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
