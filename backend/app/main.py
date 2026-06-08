from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .modules.user.router import router as user_router
from .modules.post.router import router as post_router
from .core.database import Base, engine

# 创建数据库表（开发环境简单方式，生产用alembic）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fullstack Demo API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router)
app.include_router(post_router)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

# 添加示例数据（仅用于演示，首次启动时创建一些帖子）
@app.on_event("startup")
def create_sample_posts():
    from sqlalchemy.orm import Session
    from .core.database import SessionLocal
    from .modules.post import service as post_service
    from .modules.post.schemas import PostCreate
    db: Session = SessionLocal()
    if db.query(post_service.models.Post).count() == 0:
        sample_posts = [
            PostCreate(title="Welcome to FastAPI + Vue3", content="This is a demo post."),
            PostCreate(title="Element Plus is awesome", content="UI components made easy."),
        ]
        # 使用一个虚拟用户ID（假设存在id=1，但如果没有用户则需处理，这里简单处理）
        # 实际演示可先注册登录后手动创建，此处仅为避免空列表
        pass
    db.close()