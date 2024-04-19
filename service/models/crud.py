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

def update_company(db: Session, company_id: int, company_update: schemas.CompanyUpdate):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company:
        for field, value in company_update.dict(exclude_unset=True).items():
            setattr(company, field, value)
        db.commit()
        db.refresh(company)
        return company
    
def delete_company(db: Session, company_id: int):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company:
        db.delete(company)
        db.commit()
        return company

#  gets all of the carbon offsets of a particular company given the company ID
def get_carbon_offsets(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.CarbonOffset).filter(models.CarbonOffset.company_id == company_id).offset(skip).limit(limit).all()

# creates a carbon offset for a speficied company
def create_carbon_offset(db: Session, carbon_offset: schemas.CarbonOffsetCreate):
    db_carbon_offset = models.CarbonOffset(**carbon_offset.dict())
    db.add(db_carbon_offset)
    db.commit()
    db.refresh(db_carbon_offset)
    return db_carbon_offset

def get_carbon_offset(db: Session, carbon_offset_id: int):
    return db.query(models.CarbonOffset).filter(models.CarbonOffset.id == carbon_offset_id).first()


def update_carbon_offset(db: Session, carbon_offset_id: int, carbon_offset_update: schemas.CarbonOffsetUpdate):
    """
    Update a carbon offset entry.

    Args:
        carbon_offset_update (CarbonOffsetUpdate): Data to update the carbon offset.
        carbon_offset_id (int): ID of the associated offset.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonOffset: The updated carbon offset.
    """
    db_carbon_offset = get_carbon_offset(db, carbon_offset_id)
    if db_carbon_offset:
        for field, value in carbon_offset_update.dict(exclude_unset=True).items():
            setattr(db_carbon_offset, field, value)
        db.commit()
        db.refresh(db_carbon_offset)
    return db_carbon_offset

def delete_carbon_offset(db: Session, carbon_offset_id: int):
    """
    Delete a carbon offset entry.

    Args:
        carbon_offset_id: ID of the carbon offset to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonOffset: The updated carbon offset.
    """
    db_carbon_offset = get_carbon_offset(db, carbon_offset_id)
    if db_carbon_offset:
        db.delete(db_carbon_offset)
        db.commit()
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
def get_company_branches(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.CompanyBranch).filter(models.CompanyBranch.company_id == company_id).offset(skip).limit(limit).all()

# creates a company branch associated under a specified company
def create_company_branch(db: Session, company_branch: schemas.CompanyBranchCreate):
    db_company_branch = models.CompanyBranch(**company_branch.dict())
    db.add(db_company_branch)
    db.commit()
    db.refresh(db_company_branch)
    return db_company_branch

def update_branch(db: Session, branch_id: int, branch_update: schemas.CompanyBranchUpdate):
    branch = db.query(models.CompanyBranch).filter(models.CompanyBranch.id == branch_id).first()
    if branch:
        for field, value in branch_update.dict(exclude_unset=True).items():
            setattr(branch, field, value)
        db.commit()
        db.refresh(branch)
        return branch
    
def delete_branch(db: Session, branch_id: int):
    branch = db.query(models.CompanyBranch).filter(models.CompanyBranch.id == branch_id).first()
    if branch:
        db.delete(branch)
        db.commit()
        return branch

# gets all carbon emission sources associated with a specific branch
def get_carbon_emissions_sources(db: Session, branch_id: int):
    return db.query(models.CarbonEmissionsSource).filter(models.CarbonEmissionsSource.branch_id == branch_id).offset(skip).limit(limit).all()


def create_carbon_emissions_source(db: Session, emissions_source: schemas.CarbonEmissionsSourceCreate):
    db_emissions_source = models.CarbonEmissionsSource(**emissions_source.dict())
    db.add(db_emissions_source)
    db.commit()
    db.refresh(db_emissions_source)
    return db_emissions_source

def update_carbon_emissions_source(db: Session, source_id: int, source_update: schemas.CarbonEmissionsSourceUpdate):
    db_source = get_carbon_emissions_source(db, source_id)
    if db_source:
        for field, value in source_update.dict(exclude_unset=True).items():
            setattr(db_source, field, value)
        db.commit()
        db.refresh(db_source)
    return db_source

def delete_carbon_emissions_source(db: Session, source_id: int):
    db_source = get_carbon_emissions_source(db, source_id)
    if db_source:
        db.delete(db_source)
        db.commit()
    return db_source

def get_carbon_emissions_source(db: Session, source_id: int):
    return db.query(models.CarbonEmissionsSource).filter(models.CarbonEmissionsSource.id == source_id).first()


def get_carbon_regulations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CarbonRegulation).offset(skip).limit(limit).all()


def create_carbon_regulation(db: Session, regulation: schemas.CarbonRegulationCreate):
    db_regulation = models.CarbonRegulation(**regulation.dict())
    db.add(db_regulation)
    db.commit()
    db.refresh(db_regulation)
    return db_regulation

def delete_regulation(db: Session, regulation_id: int):
    regulation = db.query(models.CarbonRegulation).filter(models.CarbonRegulation.id == regulation_id).first()
    if regulation:
        db.delete(regulation)
        db.commit()
        return regulation
    return None

def update_regulation(db: Session, regulation_id: int, regulation_update: schemas.CarbonRegulationUpdate):
    regulation = db.query(models.CarbonRegulation).filter(models.CarbonRegulation.id == regulation_id).first()
    if regulation:
        regulation.c_name = regulation_update.c_name
        regulation.description = regulation_update.description
        db.commit()
        db.refresh(regulation)
        return regulation
    return None
    

def get_regulation_by_id(db: Session, regulation_id: int):
    return db.query(models.Company).filter(models.CarbonRegulation.id == regulation_id).first()


def get_carbon_footprints(db: Session, source_id: int):
    return db.query(models.CarbonFootprint).filter(models.CarbonFootprint.source_id == source_id).offset(skip).limit(limit).all()


def create_carbon_footprint(db: Session, footprint: schemas.CarbonFootprintCreate):
    db_footprint = models.CarbonFootprint(**footprint.dict())
    db.add(db_footprint)
    db.commit()
    db.refresh(db_footprint)
    return db_footprint

def get_carbon_sequestrations(db: Session, source_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.CarbonSequestration).filter(models.CarbonSequestration.source_id == source_id).offset(skip).limit(limit).all()


def create_carbon_sequestration(db: Session, sequestration: schemas.CarbonSequestrationCreate):
    db_sequestration = models.CarbonFootprint(**sequestration.dict())
    db.add(db_sequestration)
    db.commit()
    db.refresh(db_sequestration)
    return db_sequestration


def get_emission_source_by_ids(db: Session, company_id: int, branch_id: int, emission_source_id: int):
    """
    Get a specific emission source by company ID, branch ID, and emission source ID.

    Args:
        db (Session): SQLAlchemy database session.
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.

    Returns:
        models.CarbonEmissionsSource: The retrieved emission source, or None if not found.
    """
    return db.query(models.CarbonEmissionsSource).filter(
        models.CarbonEmissionsSource.id == emission_source_id,
        models.CarbonEmissionsSource.branch_id == branch_id,
        models.CompanyBranch.company_id == company_id
    ).first()


def get_sequestration_by_ids(db: Session, company_id: int, branch_id: int, emission_source_id: int, sequestration_id: int):
    """
    Get a specific sequestration entry by company ID, branch ID, emission source ID, and sequestration ID.

    Args:
        db (Session): SQLAlchemy database session.
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        sequestration_id (int): ID of the sequestration entry within the emission source.

    Returns:
        models.CarbonSequestration: The retrieved sequestration entry, or None if not found.
    """
    return db.query(models.CarbonSequestration).filter(
        models.CarbonSequestration.id == sequestration_id,
        models.CarbonSequestration.source_id == emission_source_id,
        models.CarbonEmissionsSource.id == emission_source_id,
        models.CompanyBranch.id == branch_id,
        models.CompanyBranch.company_id == company_id
    ).first()

def update_sequestration(db: Session, sequestration: models.CarbonSequestration, sequestration_update: schemas.CarbonSequestrationUpdate):
    """
    Update a sequestration entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        sequestration (models.CarbonSequestration): Sequestration entry to update.
        sequestration_update (schemas.CarbonSequestrationUpdate): Updated data for the sequestration entry.

    Returns:
        models.Sequestration: The updated sequestration entry.
    """
    for value in sequestration_update.dict(exclude_unset=True).items():
        setattr(sequestration, value)
    db.commit()
    db.refresh(sequestration)
    return sequestration

def create_sequestration(db: Session, sequestration: schemas.CarbonSequestrationCreate, emission_source_id: int):
    """
    Create a new sequestration entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        sequestration (schemas.SequestrationCreate): Data for creating the sequestration entry.
        emission_source_id (int): ID of the emission source associated with the sequestration.

    Returns:
        models.CarbonSequestration: The created sequestration entry.
    """
    db_sequestration = models.CarbonSequestration(**sequestration.dict(), source_id=emission_source_id)
    db.add(db_sequestration)
    db.commit()
    db.refresh(db_sequestration)
    return db_sequestration

def get_carbon_sequestration(db: Session, seq_id: int):
    return db.query(models.CarbonSequestration).filter(models.CarbonSequestration.id == seq_id).first()

# Function to delete a carbon sequestration entry
def delete_carbon_sequestration(db: Session, seq_id: int):
    db_seq = get_carbon_sequestration(db, seq_id)
    if db_seq:
        db.delete(db_seq)
        db.commit()
    return db_seq


def create_carbon_footprint(db: Session, carbon_footprint: schemas.CarbonFootprintCreate, emission_source_id: int):
    """
    Create a new carbon footprint entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        carbon_footprint (schemas.CarbonFootprintCreate): Data for creating the carbon footprint entry.
        emission_source_id (int): ID of the emission source associated with the carbon footprint.

    Returns:
        models.CarbonFootprint: The created carbon footprint entry.
    """
    db_carbon_footprint = models.CarbonFootprint(**carbon_footprint.dict(), source_id=emission_source_id)
    db.add(db_carbon_footprint)
    db.commit()
    db.refresh(db_carbon_footprint)
    return db_carbon_footprint


def get_carbon_footprint_by_ids(db: Session, company_id: int, branch_id: int, emission_source_id: int, carbon_footprint_id: int):
    """
    Get a specific carbon footprint entry by company ID, branch ID, emission source ID, and carbon footprint ID.

    Args:
        db (Session): SQLAlchemy database session.
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        carbon_footprint_id (int): ID of the carbon footprint entry within the emission source.

    Returns:
        models.CarbonFootprint: The retrieved carbon footprint entry, or None if not found.
    """
    return db.query(models.CarbonFootprint).filter(
        models.CarbonFootprint.id == carbon_footprint_id,
        models.CarbonFootprint.source_id == emission_source_id,
        models.CarbonEmissionsSource.id == emission_source_id,
        models.CompanyBranch.id == branch_id,
        models.CompanyBranch.company_id == company_id
    ).first()

def update_carbon_footprint(db: Session, carbon_footprint: models.CarbonFootprint, carbon_footprint_update: schemas.CarbonFootprintUpdate):
    """
    Update a carbon footprint entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        carbon_footprint (models.CarbonFootprint): Carbon footprint entry to update.
        carbon_footprint_update (schemas.CarbonFootprintUpdate): Updated data for the carbon footprint entry.

    Returns:
        models.CarbonFootprint: The updated carbon footprint entry.
    """
    for value in carbon_footprint_update.dict(exclude_unset=True).items():
        setattr(carbon_footprint, value)
    db.commit()
    db.refresh(carbon_footprint)
    return carbon_footprint

def get_carbon_footprint(db: Session, footprint_id: int):
    return db.query(models.CarbonFootprint).filter(models.CarbonFootprint.id == footprint_id).first()


# Function to delete a carbon footprint entry
def delete_carbon_footprint(db: Session, footprint_id: int):
    db_footprint = get_carbon_footprint(db, footprint_id)
    if db_footprint:
        db.delete(db_footprint)
        db.commit()
    return db_footprint