"""Async models using SQLModel for FastAPI.

These mirror the earlier `models.py` but use `sqlmodel.SQLModel` so they are
ready for async operations and work smoothly with FastAPI and Pydantic.
"""
from __future__ import annotations

from typing import Optional, List
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    brief: Optional[str] = None
    created_at: Optional[datetime] = None

    boq_items: List["BOQItem"] = Relationship(back_populates="project")


class BOQItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    item_name: str
    unit: Optional[str] = None
    quantity: Optional[float] = None
    unit_rate: Optional[float] = None
    confidence: Optional[float] = None
    metadata: Optional[dict] = None

    project: Optional[Project] = Relationship(back_populates="boq_items")


class RateSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    source_type: Optional[str] = None
    url: Optional[str] = None
    credibility: Optional[float] = None


class RateCache(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item: str = Field(index=True)
    median: Optional[float] = None
    confidence: Optional[float] = None
    source_url: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    raw_samples: Optional[dict] = None


class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    meta: Optional[dict] = None


class RFQ(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    vendor_id: int = Field(foreign_key="vendor.id")
    status: str = "draft"
    sent_at: Optional[datetime] = None
    payload: Optional[dict] = None


class Quote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rfq_id: int = Field(foreign_key="rfq.id")
    vendor_id: int = Field(foreign_key="vendor.id")
    amount: Optional[float] = None
    received_at: Optional[datetime] = None
    meta: Optional[dict] = None


class AgentRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_name: str
    input: Optional[dict] = None
    output: Optional[dict] = None
    created_at: Optional[datetime] = None


class ClarificationQuestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    question_text: str
    options: Optional[List[str]] = None
    response: Optional[str] = None
    asked_at: Optional[datetime] = None
