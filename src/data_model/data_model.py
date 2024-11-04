from pydantic import BaseModel
from datetime import datetime

class RepoInfo(BaseModel):
    repo_name: str
    last_updated: datetime
    hash: str
    author: str
    message: str