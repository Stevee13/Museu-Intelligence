from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Opportunity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    agency_name: str
    source_url: str
    submission_deadline: Optional[datetime] = None
    max_budget: Optional[float] = None
    score: int = Field(..., ge=1, le=5)
    justification: str

