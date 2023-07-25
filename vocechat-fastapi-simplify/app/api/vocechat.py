from fastapi import BackgroundTasks
from fastapi import APIRouter


# 引用utils中的方法
from app.utils.bot_vocechat import *
# 引用models中的方法model
from app.models.vocechat import *


# 构建app
router = APIRouter()


# 验证连接
@router.get("/voce/bot", tags=["VoceChat"])
async def voce_get_bot():
    return {"status": "OK"}


# 连接
@router.post("/voce/bot", tags=["VoceChat"])
async def voce_post_bot(data: VoceMsg, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_msg_handler, data)
    return {"status": "OK"}

  
async def run_msg_handler(data):
    handler = MessageHandler(data)
    handler.handle()


    
