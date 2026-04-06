from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from services.github import github_service

router = APIRouter()


# ---------- response models ----------

class UserOut(BaseModel):
    login: str
    html_url: str


class IssueOut(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
    body: str | None
    user: UserOut


# ---------- request model ----------

class CreateIssueIn(BaseModel):
    owner: str = Field(..., examples=["octocat"])
    repo: str = Field(..., examples=["Hello-World"])
    title: str = Field(..., min_length=1, examples=["Bug: something broke"])
    body: str = Field(default="", examples=["Steps to reproduce..."])


# ---------- routes ----------

@router.get("/issues", response_model=list[IssueOut], summary="List issues for a repo")
async def list_issues(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
):
    return await github_service.list_issues(owner, repo)


@router.post("/create-issue", response_model=IssueOut, status_code=201, summary="Create a new issue")
async def create_issue(payload: CreateIssueIn):
    return await github_service.create_issue(
        payload.owner, payload.repo, payload.title, payload.body
    )