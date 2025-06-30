from fastapi.applications import FastAPI

from examples.file_upload.routes import router as file_upload_router
from examples.websocket.routes import router as websocket_router

app = FastAPI(
    description='FastAPI Examples',
)

app.include_router(file_upload_router)
app.include_router(websocket_router)
