from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.upload import router as api_router
from app.ui.routes import router as ui_router

app = FastAPI()

# Mount the static files (CSS and JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API and UI routers
app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(ui_router, tags=["ui"])

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
