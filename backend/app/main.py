from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .services import setup_data
from .database import engine, Base

app = FastAPI(title="Edu Equity Local API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
setup_data()

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Local Edu Equity API running!"}
