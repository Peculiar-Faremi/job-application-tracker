from fastapi import FastAPI
from app.routers import applications, users,auth
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.redis_client import r

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    r.close() #it hands the connection back
    r.connection_pool.disconnect() #it actually closes every socket in the pool.

app=FastAPI(lifespan=lifespan) #use the lifespan function defined above
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #permission to allow any website talk to me (for now until the frontend is launched)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(applications.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}