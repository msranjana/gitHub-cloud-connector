from fastapi import FastAPI
from routes import repos_router, issues_router

app = FastAPI(
    title="GitHub Cloud Connector",
    description="A minimal connector to integrate with the GitHub REST API.",
    version="1.0.0",
)

app.include_router(repos_router, tags=["Repositories"])
app.include_router(issues_router, tags=["Issues"])


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}