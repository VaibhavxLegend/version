# app/models/db_models.py
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)  # UUID string
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    filename = Column(String, nullable=True)
    md_content = Column(Text, nullable=True)  # Markdown text extracted from PDF
    original_blob_hash = Column(String, unique=True, nullable=True)  # For deduplication

    chunks = relationship("DocumentChunk", back_populates="document")
    sessions = relationship("Session", back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, index=True)  # UUID string
    document_id = Column(String, ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    # Store Pinecone vector ID or metadata reference if needed
    pinecone_id = Column(String, unique=True, nullable=True)

    document = relationship("Document", back_populates="chunks")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)  # UUID string
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="sessions")
    queries = relationship("Query", back_populates="session")


class Query(Base):
    __tablename__ = "queries"

    id = Column(String, primary_key=True, index=True)  # UUID string
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    rationale = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="queries")
    sources = relationship("ClauseSource", back_populates="query")


class ClauseSource(Base):
    __tablename__ = "clause_sources"

    id = Column(String, primary_key=True, index=True)  # UUID string
    query_id = Column(String, ForeignKey("queries.id"), nullable=False)
    clause_text = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    confidence = Column(Float, nullable=True)

    query = relationship("Query", back_populates="sources")
