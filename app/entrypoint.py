import uvicorn
from fastapi import FastAPI
from settings import get_settings
from routers.admin.admin import router

setts = get_settings()

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=setts.APP_PORT, log_level="info")
