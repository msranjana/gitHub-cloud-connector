from fastapi import APIRouter, Query
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


class CommitAuthorOut(BaseModel):
    name: str
    email: str
    date: str


class CommitMetaOut(BaseModel):
    message: str
    author: CommitAuthorOut | None = None


class CommitOut(BaseModel):
    sha: str
    html_url: str
    commit: CommitMetaOut


@router.get("/repos", response_model=list[RepoOut], summary="List authenticated user's repositories")
async def list_repos():
    return await github_service.get_repos()


@router.get("/commits", response_model=list[CommitOut], summary="List commits for a repository")
async def list_commits(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    per_page: int = Query(30, ge=1, le=100, description="Max commits per page"),
    sha: str | None = Query(None, description="Branch name or commit SHA to filter from"),
):
    return await github_service.list_commits(owner, repo, per_page=per_page, sha=sha)
