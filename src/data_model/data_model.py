from pydantic import BaseModel
from datetime import datetime
from typing import List


class RepoInfo(BaseModel):
    repo_name: str
    last_updated: datetime
    hash: str
    author: str
    message: str


class RepoInfoDetails(BaseModel):
    repo_name: str
    creation_date: str
    weekly_commit_num: List[int]
    week_label: List[str]
    commits_by_day_counts: List[int]
    commits_by_hour_counts: List[int]
    contributions_by_contributors: List[str]
    contribution_counts: List[int]
