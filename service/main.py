from fastapi import FastAPI, APIRouter, HTTPException, Depends
from models import crud
from sqlalchemy.orm import Session

# from app.models.user import User, UserCreate, UserUpdate
# from app.dependencies.database import get_database, Database
from models import models, schemas
from models.database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
router = APIRouter()


@router.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company.

    Args:
        company (CompanyCreate): Data to create the company.
        db (Session): SQLAlchemy database session.

    Returns:
        Company: The created company.
    Raises:
        HTTPException: If the company with the given name is already present in the database.
    """
    db_company = crud.get_company_by_name(db, c_name=company.c_name)
    if db_company:
        raise HTTPException(status_code=400, detail="company already added")
    return crud.create_company(db=db, company=company)


# Get company from id endpoint
@router.get("/company/{company_id}", response_model=schemas.Company)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """
    Get a company from its ID.

    Args:
        company_id : The company's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        Company: The company with the specified ID.
    Raises:
        HTTPException: If the company with the given name is not present in the database.
    """
    db_company = crud.get_company_by_cid(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=400, detail="Company not found")
    return db_company

# Get all companies endpoint
@router.get("/companies/", response_model=List[schemas.Company])
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all companies from the database.

    Args:
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.Company]: A list of company objects.
    """
    companies = crud.get_companies(db=db, skip=skip, limit=limit)
    return companies


@app.put("/company/{company_id}", response_model=schemas.Company)
def update_company(company_id: int, company_update: schemas.CompanyUpdate, db: Session = Depends(get_db)):
    """
    Update an existing company.

    Args:
        company_id (int): ID of the company to update.
        company_update (schemas.CompanyUpdate): Updated data for the company.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Company: The updated company.
    """
    updated_company = crud.update_company(db=db, company_id=company_id, company_update=company_update)
    if updated_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated_company

@app.delete("/company/{company_id}", response_model=schemas.Company)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing company.

    Args:
        company_id (int): ID of the company to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Company: The deleted company.
    """
    deleted_company = crud.delete_company(db=db, company_id=company_id)
    if deleted_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return deleted_company


@router.post("/carbon_offsets/", response_model=schemas.CarbonOffset)
def create_carbon_offset(offset: schemas.CarbonOffsetCreate, db: Session = Depends(get_db)):
    """
    Create a new carbon offset entry.

    Args:
        offset (CarbonOffsetCreate): Data to create the carbon offset.
        company_id (int): ID of the associated company.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonOffset: The created carbon offset.
    Raises:
        HTTPException: If the company with the given ID is not found.
    """
    db_company = crud.get_company_by_cid(db, company_id=offset.company_id)
    if db_company is None:
        raise HTTPException(status_code=400, detail="Invalid company ID")
    return crud.create_carbon_offset(db=db, carbon_offset=offset)


@router.get("/companies/{company_id}/carbon_offsets/", response_model=List[schemas.CarbonOffset])
def read_carbon_offsets(company_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Get all carbon offsets of a specific company.

    Args:
        company_id : The company's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.Company]: A list of carbon offset objects.
    Raises:
        HTTPException: If the company with the given ID is not found.
    """
    db_company = crud.get_company_by_cid(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=400, detail="Company not found")
    offsets = crud.get_carbon_offsets(db=db, company_id=company_id, skip=skip, limit=limit)
    return offsets


@app.put("/branch/{branch_id}", response_model=schemas.CompanyBranch)
def update_branch(branch_id: int, branch_update: schemas.CompanyBranchUpdate, db: Session = Depends(get_db)):
    """
    Update an existing branch.

    Args:
        branch_id (int): ID of the branch to update.
        branch_update (schemas.BranchUpdate): Updated data for the branch.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.CompanyBranch: The updated branch.
    """
    updated_branch = crud.update_branch(db=db, branch_id=branch_id, branch_update=branch_update)
    if updated_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return updated_branch



@router.get("/companies/{company_id}/branches/", response_model=List[schemas.CompanyBranch])
def get_branches(company_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Get all the branches of a specific company.

    Args:
        company_id : The company's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.CompanyBranch]: A list of carbon offset objects.
    Raises:
        HTTPException: If the company with the given ID is not found.
    """
    db_company = crud.get_company_by_cid(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=400, detail="Company not found")
    company_branches = crud.get_company_branches(db=db, company_id=company_id, skip=skip, limit=limit)
    return company_branches


@router.post("/branches/", response_model=schemas.CompanyBranch)
def create_company_branch(branch: schemas.CompanyBranchCreate, db: Session = Depends(get_db)):
    """
    Create a new carbon offset entry.

    Args:
        offset (CarbonOffsetCreate): Data to create the carbon offset.
        company_id (int): ID of the associated company.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonOffset: The created carbon offset.
    Raises:
        HTTPException: If the company with the given ID is not found.
    """
    db_company = crud.get_company_by_cid(db, company_id=branch.company_id)
    if db_company is None:
        raise HTTPException(status_code=400, detail="Invalid company ID")
    
    # Not currently possible to get company from branch
    # db_branch = crud.get_company_branch(db, branch_id=branch_id)
    # if db_branch:
    #     raise HTTPException(status_code=400, detail="Branch already exists in DB")
    return crud.create_company_branch(db=db, company_branch=branch)

@app.delete("/branch/{branch_id}", response_model=schemas.CompanyBranch)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing branch.

    Args:
        branch_id (int): ID of the branch to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.CompanyBranch: The deleted branch.
    """
    deleted_branch = crud.delete_branch(db=db, branch_id=branch_id)
    if deleted_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return deleted_branch


@router.get("/branch/{branch_id}/emissionssources/", response_model=List[schemas.CarbonEmissionsSource])
def get_carbon_emissions_source(branch_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Get all the carbon emissions sources from a specific company branch.

    Args:
        branch_id : The branch's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.CarbonEmissionsSource]: A list of carbon emission source objects.
    Raises:
        HTTPException: If the branch with the given ID does not exist.
    """
    db_branch = crud.get_company_branch(db, branch_id=branch_id)
    if db_branch is None:
        raise HTTPException(status_code=400, detail="Invalid branch ID")
    company_branches = crud.get_carbon_emissions_sources(db=db, branch_id=branch_id, skip=skip, limit=limit)
    return company_branches


@router.post("/emissionssources/", response_model=schemas.CarbonEmissionsSource)
def create_carbon_emissions_source(emissions_source: schemas.CarbonEmissionsSourceCreate, db: Session = Depends(get_db)):
    """
    Create a new carbon offset entry.

    Args:
        emissions_source (CarbonEmissionsSourceCreate): Data to create the carbon emissions source.
        branch_id (int): ID of the associated branch.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonEmissionsSource: The created carbon emissions source.
    Raises:
        HTTPException: If the branch with the given ID is not found.
    """
    db_branch = crud.get_company_branch(db, branch_id=emissions_source.branch_id)
    if db_branch is None:
        raise HTTPException(status_code=400, detail="Invalid branch ID")
    return crud.create_carbon_emissions_source(db=db, emissions_source=emissions_source)


@router.get("/emissionssource/{source_id}/footprints/", response_model=List[schemas.CarbonFootprint])
def get_carbon_footprints(source_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Get all the footprint transactions of a specific emissions source.

    Args:
        source_id : The emissions source's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.CarbonFootprint]: A list of carbon footprint objects.
    Raises:
        HTTPException: If the carbon emissions source with the given ID is not found.
    """
    db_footprint = crud.get_carbon_footprint(db, source_id=source_id)
    if db_footprint is None:
        raise HTTPException(status_code=400, detail="Emissions source not found")
    company_branches = crud.get_carbon_footprints(db=db, source_id=source_id, skip=skip, limit=limit)
    return company_branches


@router.post("/footprint/", response_model=schemas.CarbonFootprint)
def create_carbon_footprint(footprint: schemas.CarbonFootprintCreate, db: Session = Depends(get_db)):
    """
    Create a new carbon footprint entry.

    Args:
        footprint (CarbonFootprintCreate): Data to create the carbon footprint.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonSequestration: The created carbon footprint object.
    Raises:
        HTTPException: If the emissions source with the given ID is not found.
    """
    db_emission_sources = crud.get_carbon_emissions_sources(db, source_id=footprint.source_id)
    if db_emission_sources is None:
        raise HTTPException(status_code=400, detail="Emissions source not found")
    
    return crud.create_carbon_footprint(db=db, footprint=footprint)



@router.get("/emissionssource/{source_id}/sequestrations/", response_model=List[schemas.CarbonSequestration])
def get_carbon_sequestrations(source_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Get all the sequestration transactions of a specific emissions source.

    Args:
        source_id : The emissions source's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.CarbonSequestration]: A list of carbon sequestration objects.
    Raises:
        HTTPException: If the carbon emissions source with the given ID is not found.
    """
    db_emissions_source = crud.get_emissions_source(db, source_id=source_id)
    if db_emissions_source is None:
        raise HTTPException(status_code=400, detail="Emissions source not found")
    company_branches = crud.get_carbon_sequestrations(db=db, source_id=source_id, skip=skip, limit=limit)
    return company_branches


@router.post("/sequestration/", response_model=schemas.CarbonSequestration)
def create_carbon_sequestration(sequestration: schemas.CarbonSequestrationCreate, db: Session = Depends(get_db)):
    """
    Create a new carbon sequestration entry.

    Args:
        sequestration (CarbonSequestrationCreate): Data to create the carbon sequestration.
        db (Session): SQLAlchemy database session.

    Returns:
        CarbonSequestration: The created carbon sequestration object.
    Raises:
        HTTPException: If the emissions source with the given ID is not found.
    """
    db_emission_sources = crud.get_carbon_emissions_sources(db, source_id=sequestration.source_id)
    if db_emission_sources is None:
        raise HTTPException(status_code=400, detail="Emissions source not found")
    
    return crud.create_sequestration(db=db, sequestration=sequestration, emission_source_id=emission_source_id)


@router.post("/regulations/", response_model=schemas.CarbonRegulation)
def create_regulation(regulation: schemas.CarbonRegulationCreate, db: Session = Depends(get_db)):
    """
    Create a new regulation.

    Args:
        regulation (CarbonRegulationCreate): Data to create the regulation.
        db (Session): SQLAlchemy database session.

    Returns:
        Regulation: The created regulation.
    Raises:
        HTTPException: If the regulation with the given name is already present in the database.
    """
    db_regulation = crud.get_regulation_by_name(db, c_name=regulation.c_name)
    if db_regulation:
        raise HTTPException(status_code=400, detail="Regulation already added")
    return crud.create_regulation(db=db, regulation=regulation)


# Get regulation from id endpoint
@router.get("/regulations/{regulation_id}", response_model=schemas.CarbonRegulation)
def get_regulation(regulation_id: int, db: Session = Depends(get_db)):
    """
    Get a regulation from its ID.

    Args:
        regulation_id : The regulation's ID.
        db (Session): SQLAlchemy database session.

    Returns:
        Regulation: The regulation with the specified ID.
    Raises:
        HTTPException: If the regulation with the given name is not present in the database.
    """
    db_regulation = crud.get_regulation_by_id(db, regulation_id=regulation_id)
    if db_regulation is None:
        raise HTTPException(status_code=400, detail="Regulation not found")
    return db_regulation

# Get all regulations endpoint
@router.get("/regulations/", response_model=List[schemas.CarbonRegulation])
def get_regulations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all regulations from the database.

    Args:
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy database session.

    Returns:
        List[schemas.Regulation]: A list of regulation objects.
    """
    regulations = crud.get_carbon_regulations(db=db, skip=skip, limit=limit)
    return regulations

@router.get("/company/{company_id}/branch/{branch_id}/emissionssources/{emission_source_id}", response_model=schemas.CarbonEmissionsSource)
def read_emission_source(company_id: int, branch_id: int, emission_source_id: int, db: Session = Depends(get_db)):
    """
    Get a specific emission source by company ID, branch ID, and emission source ID.

    Args:
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.EmissionSource: The retrieved emission source.
    """
    emission_source = crud.get_emission_source_by_ids(db=db, company_id=company_id, branch_id=branch_id, emission_source_id=emission_source_id)
    if emission_source is None:
        raise HTTPException(status_code=404, detail="Emission source not found")
    return emission_source


@router.get("/company/{company_id}/branch/{branch_id}/emissionssources/{emission_source_id}/sequestration/{sequestration_id}", response_model=schemas.CarbonSequestration)
def read_sequestration(company_id: int, branch_id: int, emission_source_id: int, sequestration_id: int, db: Session = Depends(get_db)):
    """
    Get a specific sequestration entry by company ID, branch ID, emission source ID, and sequestration ID.

    Args:
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        sequestration_id (int): ID of the sequestration entry within the emission source.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Sequestration: The retrieved sequestration entry.
    """
    sequestration = crud.get_sequestration_by_ids(db=db, company_id=company_id, branch_id=branch_id, emission_source_id=emission_source_id, sequestration_id=sequestration_id)
    if sequestration is None:
        raise HTTPException(status_code=404, detail="Sequestration entry not found")
    return sequestration

@router.put("/company/{company_id}/branch/{branch_id}/emission_source/{emission_source_id}/sequestration/{sequestration_id}", response_model=schemas.CarbonSequestration)
def update_sequestration(company_id: int, branch_id: int, emission_source_id: int, sequestration_id: int, sequestration_update: schemas.CarbonSequestrationUpdate, db: Session = Depends(get_db)):
    """
    Update a specific sequestration entry by company ID, branch ID, emission source ID, and sequestration ID.

    Args:
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        sequestration_id (int): ID of the sequestration entry within the emission source.
        sequestration_update (schemas.SequestrationUpdate): Updated data for the sequestration entry.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Sequestration: The updated sequestration entry.
    """
    existing_sequestration = crud.get_sequestration_by_ids(db=db, company_id=company_id, branch_id=branch_id, emission_source_id=emission_source_id, sequestration_id=sequestration_id)
    if existing_sequestration is None:
        raise HTTPException(status_code=404, detail="Sequestration entry not found")

    updated_sequestration = crud.update_sequestration(db=db, sequestration=existing_sequestration, sequestration_update=sequestration_update)
    return updated_sequestration


@router.get("/company/{company_id}/branch/{branch_id}/emissionssources/{emission_source_id}/carbon_footprint/{carbon_footprint_id}", response_model=schemas.CarbonFootprint)
def read_carbon_footprint(company_id: int, branch_id: int, emission_source_id: int, carbon_footprint_id: int, db: Session = Depends(get_db)):
    """
    Get a specific carbon footprint entry by company ID, branch ID, emission source ID, and carbon footprint ID.

    Args:
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        carbon_footprint_id (int): ID of the carbon footprint entry within the emission source.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.CarbonFootprint: The retrieved carbon footprint entry.
    """
    carbon_footprint = crud.get_carbon_footprint_by_ids(db=db, company_id=company_id, branch_id=branch_id, emission_source_id=emission_source_id, carbon_footprint_id=carbon_footprint_id)
    if carbon_footprint is None:
        raise HTTPException(status_code=404, detail="Carbon footprint entry not found")
    return carbon_footprint


@router.put("/company/{company_id}/branch/{branch_id}/emission_source/{emission_source_id}/carbon_footprint/{carbon_footprint_id}", response_model=schemas.CarbonFootprint)
def update_carbon_footprint(company_id: int, branch_id: int, emission_source_id: int, carbon_footprint_id: int, carbon_footprint_update: schemas.CarbonFootprintUpdate, db: Session = Depends(get_db)):
    """
    Update a specific carbon footprint entry by company ID, branch ID, emission source ID, and carbon footprint ID.

    Args:
        company_id (int): ID of the company.
        branch_id (int): ID of the branch within the company.
        emission_source_id (int): ID of the emission source within the branch.
        carbon_footprint_id (int): ID of the carbon footprint entry within the emission source.
        carbon_footprint_update (schemas.CarbonFootprintUpdate): Updated data for the carbon footprint entry.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.CarbonFootprint: The updated carbon footprint entry.
    """
    existing_carbon_footprint = crud.get_carbon_footprint_by_ids(db=db, company_id=company_id, branch_id=branch_id, emission_source_id=emission_source_id, carbon_footprint_id=carbon_footprint_id)
    if existing_carbon_footprint is None:
        raise HTTPException(status_code=404, detail="Carbon footprint entry not found")

    updated_carbon_footprint = crud.update_carbon_footprint(db=db, carbon_footprint=existing_carbon_footprint, carbon_footprint_update=carbon_footprint_update)
    return updated_carbon_footprint


app.include_router(router)