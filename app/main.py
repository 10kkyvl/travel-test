from fastapi import FastAPI

from app.api.routes import places, projects

app = FastAPI(title="Travel Planner API")

app.include_router(projects.router)
app.include_router(places.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
