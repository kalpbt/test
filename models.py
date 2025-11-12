"""ORM models for ProcureMind core entities.

This schema is intentionally concise but covers the major concepts in the
presentation flow: Project, BOQItem, RateSource, RateCache, Vendor, RFQ, Quote,
AgentRun, and ClarificationQuestion. It is easy to extend later.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    JSON,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

from db import Base as DBBase


class Base(DBBase):
    __abstract__ = True


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brief: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    boq_items: Mapped[List["BOQItem"]] = relationship("BOQItem", back_populates="project", cascade="all, delete-orphan")


class BOQItem(Base):
    __tablename__ = "boq_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(300), nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    quantity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    project: Mapped[Project] = relationship("Project", back_populates="boq_items")


class RateSource(Base):
    __tablename__ = "rate_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # e.g. 'cpwd','scrape','user'
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    credibility: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class RateCache(Base):
    __tablename__ = "rate_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    median: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    raw_samples: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_email: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class RFQ(Base):
    __tablename__ = "rfqs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(Integer, ForeignKey("vendors.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="draft")
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    vendor: Mapped[Vendor] = relationship("Vendor")
    project: Mapped[Project] = relationship("Project")


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rfq_id: Mapped[int] = mapped_column(Integer, ForeignKey("rfqs.id"), nullable=False)
    vendor_id: Mapped[int] = mapped_column(Integer, ForeignKey("vendors.id"), nullable=False)
    amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    received_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    vendor: Mapped[Vendor] = relationship("Vendor")
    rfq: Mapped[RFQ] = relationship("RFQ")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(200), nullable=False)
    input: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    output: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ClarificationQuestion(Base):
    __tablename__ = "clarifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    response: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    asked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    project: Mapped[Project] = relationship("Project")
