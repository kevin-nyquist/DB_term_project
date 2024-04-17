from sqlalchemy.types import Integer, String, Date, Enum, Float
from sqlalchemy import Column, ForeignKey
import enum
from sqlalchemy.orm import relationship

from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    c_name = Column(String, index=True)

    carbon_offsets = relationship("CarbonOffset", back_populates="company")
    branches = relationship("CompanyBranch", back_populates="company")


class OffsetType(enum.Enum):
    renewable_energy_projects = 1
    reforestation = 2


class CarbonOffset(Base):
    __tablename__ = "carbon_offsets"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    offset_type = Column(Enum(OffsetType), index=True)
    offset_amount = Column(Integer, index=True)
    date = Column(Date, index=True)

    company = relationship("Company", back_populates="carbon_offsets")


class CompanyBranch(Base):
    __tablename__ = "company_branches"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    branch_name = Column(String, index=True)

    company = relationship("Company", back_populates="branches")
    emission_sources = relationship("CarbonEmissionsSource", back_populates="branch")


class CarbonEmissionsSource(Base):
    __tablename__ = "carbon_emissions_sources"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("company_branches.id"))
    source_type = Column(String, index=True)
    total_emission_value = Column(Float, index=True)
    
    branch = relationship("CompanyBranch", back_populates="emission_sources")
    footprints = relationship("CarbonFootprint", back_populates="source")
    

class CarbonRegulation(Base):
    __tablename__ = "carbon_regulations"
    
    id = Column(Integer, primary_key=True, index=True)
    regulation_name = Column(String, index=True)
    description = Column(String, index=True)


class CarbonFootprint(Base): 
    __tablename__ = "carbon_footprints"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("carbon_emissions_sources.id"))
    footprint_value = Column(Float, index=True)
    
    source = relationship("CarbonEmissionsSource", back_populates="footprints")
