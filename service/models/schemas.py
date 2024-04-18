import datetime
from sqlite3 import Date
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Company
class CompanyBase(BaseModel):
    c_name: str


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


# CarbonOffset
class OffsetType(str, Enum):
    renewable_energy_projects = "renewable_energy_projects"
    reforestation = "reforestation"

class CarbonOffsetBase(BaseModel):
    offset_type: OffsetType
    offset_amount: int
    date: Optional[str]
    

class CarbonOffsetCreate(CarbonOffsetBase):
    company_id: int


class CarbonOffset(CarbonOffsetBase):
    id: int
    company_id: int

    class Config:
        orm_mode = True


# CompanyBranch
class CompanyBranchBase(BaseModel):
    branch_name: str


class CompanyBranchCreate(CompanyBranchBase):
    company_id: int


class CompanyBranch(CompanyBranchBase):
    id: int
    company_id: int

    class Config:
        orm_mode = True


# CarbonEmissionsSource
class CarbonEmissionsSourceBase(BaseModel):
    source_type: str
    total_emission_value: float


class CarbonEmissionsSourceCreate(CarbonEmissionsSourceBase):
    branch_id: int


class CarbonEmissionsSource(CarbonEmissionsSourceBase):
    id: int
    branch_id: int

    class Config:
        orm_mode = True


# CarbonRegulation
class CarbonRegulationBase(BaseModel):
    regulation_name: str
    description: str


class CarbonRegulationCreate(CarbonRegulationBase):
    pass


class CarbonRegulation(CarbonRegulationBase):
    id: int

    class Config:
        orm_mode = True


# CarbonFootprint
class CarbonFootprintBase(BaseModel):
    footprint_value: float


class CarbonFootprintCreate(CarbonFootprintBase):
    source_id: int


class CarbonFootprint(CarbonFootprintBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True


# CarbonSequestration
class CarbonSequestrationBase(BaseModel):
    seq_value: float


class CarbonSequestrationCreate(CarbonSequestrationBase):
    source_id: int


class CarbonSequestration(CarbonSequestrationBase):
    id: int
    source_id: int

    class Config:
        orm_mode = True
