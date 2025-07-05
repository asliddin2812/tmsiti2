from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from core.database import Base

class ConstructionNorm(Base):
    __tablename__ = "construction_norms"

    id = Column(Integer, primary_key=True, index=True)
    subsystem = Column(String, nullable=False)
    group = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Standard(Base):
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class BuildingRegulation(Base):
    __tablename__ = "building_regulations"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CostResourceNorm(Base):
    __tablename__ = "cost_resource_norms"

    id = Column(Integer, primary_key=True, index=True)
    srn_code = Column(String, nullable=False, unique=True)
    srn_title = Column(String, nullable=False)
    main_shnq_code = Column(String, nullable=False)
    main_shnq_title = Column(String, nullable=False)
    additional_shnqs = Column(JSON, nullable=True)
    file = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TechnicalRegulation(Base):
    __tablename__ = "technical_regulations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())