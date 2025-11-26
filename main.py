from fastapi import FastAPI
import uvicorn


# from core.database import init_db
from api.router_assign import router as assign_router

app = FastAPI(title="idf exam")

app.include_router(assign_router)


# @app.on_event("startup")
# def on_startup():
#     init_db()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
