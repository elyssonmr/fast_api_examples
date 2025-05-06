from fastapi.applications import FastAPI

from examples.file_upload.routes import router as file_upload_router

app = FastAPI(
    description='FastAPI Examples',
)

app.include_router(file_upload_router)
