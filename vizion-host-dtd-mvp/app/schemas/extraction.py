from typing import Literal

from pydantic import BaseModel, Field


class DetectedTask(BaseModel):
    task: str
    status: Literal["new", "active", "blocked", "completed"] = "new"
    urgency: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "MEDIUM"


class DetectedBlocker(BaseModel):
    blocker: str
    type: Literal["internal", "external", "resource", "decision", "dependency", "unclear"] = "unclear"
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "MEDIUM"


class ExtractionResult(BaseModel):
    input_type: Literal[
        "QUICK_TASK",
        "COGNITIVE_DUMP",
        "EXECUTION_BLOCK",
        "DAILY_RECAP_REQUEST",
        "GENERAL_CONTEXT",
    ]
    summary: str
    category: str
    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    detected_tasks: list[DetectedTask] = Field(default_factory=list)
    detected_blockers: list[DetectedBlocker] = Field(default_factory=list)
    detected_topics: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    drift_signal: Literal["NONE", "LOW", "MEDIUM", "HIGH"] = "NONE"
    response_to_user: str
