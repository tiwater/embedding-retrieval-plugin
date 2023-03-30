from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Source(str, Enum):
    email = "email"
    file = "file"
    chat = "chat"

class Scope(str, Enum):
    public = "public"
    org = "org"
    personal = "personal"


class DocumentMetadata(BaseModel):
    source: Optional[Source] = None
    source_id: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    author: Optional[str] = None
    org_id: Optional[str] = None
    scope: Optional[Scope] = Scope.personal
    
class DocumentMetadataForm(DocumentMetadata):
    source: Optional[Source] = Field(None, alias="source")
    source_id: Optional[str] = Field(None, alias="source_id")
    url: Optional[str] = Field(None, alias="url")
    created_at: Optional[str] = Field(None, alias="created_at")
    author: Optional[str] = Field(None, alias="author")
    org_id: Optional[str] = Field(None, alias="org_id")
    scope: Optional[Scope] = Field(Scope.personal, alias="scope")


class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[List[float]] = None


class DocumentChunkWithScore(DocumentChunk):
    score: float


class Document(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: Optional[DocumentMetadata] = None


class DocumentWithChunks(Document):
    chunks: List[DocumentChunk]


class DocumentMetadataFilter(BaseModel):
    document_id: Optional[str] = None
    source: Optional[Source] = None
    source_id: Optional[str] = None
    author: Optional[str] = None
    start_date: Optional[str] = None  # any date string format
    end_date: Optional[str] = None  # any date string format
    org_id: Optional[str] = None


class Query(BaseModel):
    query: str
    filter: Optional[DocumentMetadataFilter] = None
    top_k: Optional[int] = 3


class QueryWithEmbedding(Query):
    embedding: List[float]


class QueryResult(BaseModel):
    query: str
    results: List[DocumentChunkWithScore]
