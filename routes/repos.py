from fastapi import APIRouter
from pydantic import BaseModel

from services.github import github_service

router = APIRouter()


class RepoOut(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: str
    description: str | None


@router.get("/repos", response_model=list[RepoOut], summary="List authenticated user's repositories")
async def list_repos():
    return await github_service.get_repos()