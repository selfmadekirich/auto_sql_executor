import uvicorn
import logging
from fastapi import FastAPI
from settings import get_settings
from routers.admin.admin import router
from routers.metadata.metadata import router as m_router
from routers.meta_extraction.routers import router as me_router
from routers.generation.routers import router as g_router
from routers.auth.routers import router as a_router
from routers.ai_profile.routers import router as ai_router
from fastapi.middleware.cors import CORSMiddleware

setts = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(m_router)
app.include_router(me_router)
app.include_router(g_router)
app.include_router(a_router)
app.include_router(ai_router)

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=setts.APP_PORT, log_level="info")
