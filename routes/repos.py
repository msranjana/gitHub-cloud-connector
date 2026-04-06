from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

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


class PullRequestOut(BaseModel):
    id: int
    number: int
    state: str
    title: str
    html_url: str


class CreatePullRequestIn(BaseModel):
    owner: str = Field(..., examples=["octocat"])
    repo: str = Field(..., examples=["Hello-World"])
    title: str = Field(..., min_length=1, examples=["Feature: add API endpoint"])
    head: str = Field(..., examples=["feature-branch"])
    base: str = Field(..., examples=["main"])
    body: str = Field(default="", examples=["This PR adds the new endpoint."])


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


@router.post(
    "/create-pull-request",
    response_model=PullRequestOut,
    status_code=201,
    summary="Create a pull request",
)
async def create_pull_request(payload: CreatePullRequestIn):
    return await github_service.create_pull_request(
        owner=payload.owner,
        repo=payload.repo,
        title=payload.title,
        head=payload.head,
        base=payload.base,
        body=payload.body,
    )