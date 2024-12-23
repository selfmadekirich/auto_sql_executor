import uvicorn
from fastapi import FastAPI
from settings import get_settings
from routers.admin.admin import router
from routers.metadata.metadata import router as m_router
from routers.meta_extraction.routers import router as me_router
from routers.generation.routers import router as g_router
from routers.auth.routers import router as a_router

setts = get_settings()

app = FastAPI()

app.include_router(router)
app.include_router(m_router)
app.include_router(me_router)
app.include_router(g_router)
app.include_router(a_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=setts.APP_PORT, log_level="info")
