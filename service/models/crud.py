from http.client import HTTPException
from sqlalchemy.orm import Session
from models import models, schemas

# gets company from company ID
def get_company_by_cid(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

# gets company by company name
def get_company_by_name(db: Session, c_name: str):
    return db.query(models.Company).filter(models.Company.c_name == c_name).first()

# gets all companies 0 - 100
def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

# creates a company object
def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

#  gets all of the carbon offsets of a particular company given the company ID
def get_carbon_offsets(db: Session, company_id: int):
    return db.query(models.CarbonOffset).filter(models.CarbonOffset.company_id == company_id).all()

# creates a carbon offset for a speficied company
def create_carbon_offset(db: Session, carbon_offset: schemas.CarbonOffsetCreate):
    db_carbon_offset = models.CarbonOffset(**carbon_offset.dict())
    db.add(db_carbon_offset)
    db.commit()
    db.refresh(db_carbon_offset)
    return db_carbon_offset

# gets the specified company branch from the branch ID
def get_company_branch(db: Session, branch_id: int):
    return db.query(models.CompanyBranch).filter(models.CompanyBranch.id == branch_id).first()

# Not currently possible: gets the specified company from the branch ID
# def get_company_by_bid(db: Session, branch_id: int):
#     branch = db.query(models.CompanyBranch).filter(models.CompanyBranch.id == branch_id).first()
#     if branch is None: 
#         raise HTTPException(status_code=400, detail="There are no associated companies with this branch ID")
#     return branch.company

# gets all of the company branches associated with a certain company ID
def get_company_branches(db: Session, company_id: int):
    return db.query(models.CompanyBranch).filter(models.CompanyBranch.company_id == company_id).all()

# creates a company branch associated under a specified company
def create_company_branch(db: Session, company_branch: schemas.CompanyBranchCreate):
    db_company_branch = models.CompanyBranch(**company_branch.dict())
    db.add(db_company_branch)
    db.commit()
    db.refresh(db_company_branch)
    return db_company_branch

# gets all carbon emission sources associated with a specific branch
def get_carbon_emissions_sources(db: Session, branch_id: int):
    return db.query(models.CarbonEmissionsSource).filter(models.CarbonEmissionsSource.branch_id == branch_id).all()


def create_carbon_emissions_source(db: Session, emissions_source: schemas.CarbonEmissionsSourceCreate):
    db_emissions_source = models.CarbonEmissionsSource(**emissions_source.dict())
    db.add(db_emissions_source)
    db.commit()
    db.refresh(db_emissions_source)
    return db_emissions_source


def get_carbon_regulations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CarbonRegulation).offset(skip).limit(limit).all()


def create_carbon_regulation(db: Session, regulation: schemas.CarbonRegulationCreate):
    db_regulation = models.CarbonRegulation(**regulation.dict())
    db.add(db_regulation)
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

def get_regulation_by_cid(db: Session, regulation_id: int):
    return db.query(models.Company).filter(models.CarbonRegulation.id == regulation_id).first()


def get_carbon_footprints(db: Session, source_id: int):
    return db.query(models.CarbonFootprint).filter(models.CarbonFootprint.source_id == source_id).all()


def create_carbon_footprint(db: Session, footprint: schemas.CarbonFootprintCreate):
    db_footprint = models.CarbonFootprint(**footprint.dict())
    db.add(db_footprint)
    db.commit()
    db.refresh(db_footprint)
    return db_footprint

def get_carbon_sequestrations(db: Session, source_id: int):
    return db.query(models.CarbonSequestration).filter(models.CarbonSequestration.source_id == source_id).all()


def create_carbon_sequestration(db: Session, sequestration: schemas.CarbonSequestrationCreate):
    db_sequestration = models.CarbonFootprint(**sequestration.dict())
    db.add(db_sequestration)
    db.commit()
    db.refresh(db_sequestration)
    return db_sequestration