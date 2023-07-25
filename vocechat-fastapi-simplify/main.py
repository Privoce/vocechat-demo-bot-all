from starlette.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

# 配置文件
from app.core.config import Settings
# 路由
from app.api import vocechat

# 实例化
app = FastAPI(title=Settings.Api["APP_NAME"])
app.mount("/static", StaticFiles(directory="static"), name="static")

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# templates
templates = Jinja2Templates(directory="templates")


# 主页
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 引入路由
app.include_router(vocechat.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host=Settings.Api["HOST"], port=Settings.Api["PORT"], reload=Settings.Api["RELOAD"])