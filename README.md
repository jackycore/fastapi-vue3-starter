# FastAPI + Vue3 + Element Plus 全栈项目

基于 **FastAPI** 和 **Vue 3** 的现代化全栈 Web 应用模板，采用模块化后端架构（业务拆分）和组件化前端开发，集成 **Element Plus** 组件库。

## ✨ 技术栈

### 后端

- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Python Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM 框架
- [Alembic](https://alembic.sqlalchemy.org/) - 数据库迁移工具
- [Pydantic](https://docs.pydantic.dev/) - 数据验证与配置管理
- [python-jose](https://github.com/mpdavis/python-jose) - JWT 身份认证
- [passlib](https://passlib.readthedocs.io/) - 密码哈希（bcrypt）

### 前端

- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Vite](https://vitejs.dev/) - 极速构建工具
- [Element Plus](https://element-plus.org/) - 基于 Vue 3 的 UI 组件库
- [Pinia](https://pinia.vuejs.org/) - Vue 状态管理
- [Vue Router](https://router.vuejs.org/) - 前端路由
- [Axios](https://axios-http.com/) - HTTP 客户端

---

## 📁 项目结构

```
project/
├── backend/ # FastAPI 后端服务
│ ├── app/
│ │ ├── core/ # 全局核心组件（配置、数据库、安全）
│ │ ├── modules/ # 业务模块（按领域拆分）
│ │ │ ├── user/ # 用户模块（models, schemas, service, router）
│ │ │ └── post/ # 文章模块
│ │ ├── utils/ # 通用工具函数
│ │ └── main.py # 应用入口
│ ├── tests/ # 单元测试
│ ├── migrations/ # Alembic 迁移脚本
│ ├── requirements.txt
│ └── .env # 环境变量
├── frontend/ # Vue3 前端应用
│ ├── public/
│ ├── src/
│ │ ├── assets/ # 静态资源
│ │ ├── components/ # 通用组件
│ │ ├── views/ # 页面组件
│ │ ├── router/ # 路由配置
│ │ ├── stores/ # Pinia 状态管理
│ │ ├── apis/ # API 请求封装
│ │ ├── App.vue
│ │ └── main.js
│ ├── index.html
│ ├── package.json
│ └── vite.config.js
└── README.md
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 pnpm

### 1. 克隆项目

```bash
git clone https://github.com/jackycore/fastapi-vue3-starter.git
cd fastapi-vue3-starter
```

### 2. 后端配置与启动

#### 2.1 创建虚拟环境并安装依赖

```
bash
cd backend
python -m venv .venv
```

##### Windows

```
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

cd frontend
nodeenv --node=22.22.3 node_venv --mirror=https://npmmirror.com/mirrors/node
```

##### macOS/Linux

```
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

cd frontend
nodeenv --node=22.22.3 node_venv --mirror=https://npmmirror.com/mirrors/node
```

#### 2.2 配置环境变量

复制 .env.example 并填写必要信息：

```bash
cp .env.example .env
.env 示例内容：
```

```env
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

#### 2.3 数据库迁移

```bash
alembic init migrations
```

# 配置 alembic.ini 中的 sqlalchemy.url 或直接使用环境变量

```
alembic revision --autogenerate -m "init"
alembic upgrade head
```

#### 2.4 启动后端服务

```bash
uvicorn app.main:app --reload --port 8000
API 文档地址：http://localhost:8000/docs
```

### 3. 前端配置与启动

#### 3.1 安装依赖

```bash
cd ../frontend
npm install
```

#### 3.2 配置代理（可选）

修改 vite.config.js 将 API 请求代理到后端：

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
```

#### 3.3 启动开发服务器

```bash
npm run dev
```

前端访问地址：http://localhost:5173

## 🔗 前后端联调

前端通过 Axios 请求 /api/xxx，Vite 代理将请求转发到 http://localhost:8000/api/xxx

后端 CORS 已配置允许前端地址 http://localhost:5173

生产环境下，前端构建产物（dist/）可放置于后端静态目录，由 FastAPI 统一托管

## 🧪 测试

后端测试

```bash
cd backend
pytest tests/
```

前端测试（若配置）

```bash
cd frontend
npm run test
```

## 📦 生产部署

构建前端：

```bash
cd frontend
npm run build
```

生成的 dist/ 目录包含所有静态文件。

将静态文件复制到后端：

```bash
cp -r frontend/dist/* backend/static/
```

配置 FastAPI 托管静态文件：
在 main.py 中添加：

```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

使用生产级服务器（如 gunicorn + uvicorn workers）：

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request。请确保代码通过 Lint 和测试。

## 📄 许可证

MIT

## 📧 联系方式

项目维护者：Jacky Lee
邮箱：389840137@qq.com
