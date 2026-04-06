from typing import Any
import httpx
from fastapi import HTTPException
from config.settings import settings


class GitHubService:
    """Reusable async client for GitHub REST API v3."""

    def __init__(self):
        self._base = settings.github_api_url
        self._headers = {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        url = f"{self._base}{path}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method, url, headers=self._headers, timeout=10.0, **kwargs
                )
            except httpx.RequestError as exc:
                raise HTTPException(status_code=503, detail=f"Network error: {exc}")

        if not response.is_success:
            detail = response.json().get("message", response.text)
            raise HTTPException(status_code=response.status_code, detail=detail)

        return response.json()

    # ---------- public methods ----------

    async def get_repos(self) -> list[dict]:
        """Fetch repos for the authenticated user."""
        return await self._request("GET", "/user/repos", params={"per_page": 100})

    async def list_issues(self, owner: str, repo: str) -> list[dict]:
        """List open issues for owner/repo."""
        return await self._request("GET", f"/repos/{owner}/{repo}/issues")

    async def create_issue(
        self, owner: str, repo: str, title: str, body: str
    ) -> dict:
        """Create a new issue in owner/repo."""
        payload = {"title": title, "body": body}
        return await self._request(
            "POST", f"/repos/{owner}/{repo}/issues", json=payload
        )

    async def list_commits(
        self,
        owner: str,
        repo: str,
        per_page: int = 30,
        sha: str | None = None,
    ) -> list[dict]:
        """List commits for owner/repo, optionally filtered by branch SHA."""
        params: dict[str, Any] = {"per_page": per_page}
        if sha:
            params["sha"] = sha
        return await self._request("GET", f"/repos/{owner}/{repo}/commits", params=params)


# Singleton — import and reuse across routes
github_service = GitHubService()