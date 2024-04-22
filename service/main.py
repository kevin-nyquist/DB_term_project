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

@app.post("/carbon_offset/", response_model=schemas.CarbonOffset)
def create_carbon_offset(carbon_offset: schemas.CarbonOffsetCreate, db: Session = Depends(get_db)):
    return crud.create_carbon_offset(db=db, carbon_offset=carbon_offset)

@app.put("/carbon_offset/{carbon_offset_id}", response_model=schemas.CarbonOffset)
def update_carbon_offset(
    carbon_offset_id: int, carbon_offset_update: schemas.CarbonOffsetUpdate, db: Session = Depends(get_db)
):
    updated_offset = crud.update_carbon_offset(db=db, carbon_offset_id=carbon_offset_id, carbon_offset_update=carbon_offset_update)
    if updated_offset is None:
        raise HTTPException(status_code=404, detail="Carbon offset not found")
    return updated_offset

@app.delete("/carbon_offset/{carbon_offset_id}", response_model=schemas.CarbonOffset)
def delete_carbon_offset(carbon_offset_id: int, db: Session = Depends(get_db)):
    deleted_offset = crud.delete_carbon_offset(db=db, carbon_offset_id=carbon_offset_id)
    if deleted_offset is None:
        raise HTTPException(status_code=404, detail="Carbon offset not found")
    return deleted_offset


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
    db_emission_source = crud.get_carbon_emissions_source(db, source_id=source_id)
    if db_emission_source is None:
        raise HTTPException(status_code=400, detail="No footprints found")
    carbon_footprints = crud.get_carbon_footprints(db=db, source_id=source_id, skip=skip, limit=limit)
    return carbon_footprints

@app.post("/emissionssource/", response_model=schemas.CarbonEmissionsSource)
def create_carbon_emissions_source(source: schemas.CarbonEmissionsSourceCreate, db: Session = Depends(get_db)):
    return crud.create_carbon_emissions_source(db=db, source=source)

@app.put("/emissionssource/{source_id}", response_model=schemas.CarbonEmissionsSource)
def update_carbon_emissions_source(
    source_id: int, source_update: schemas.CarbonEmissionsSourceUpdate, db: Session = Depends(get_db)
):
    updated_source = crud.update_carbon_emissions_source(db=db, source_id=source_id, source_update=source_update)
    if updated_source is None:
        raise HTTPException(status_code=404, detail="Carbon emissions source not found")
    return updated_source

@app.delete("/emissionssource/{source_id}", response_model=schemas.CarbonEmissionsSource)
def delete_carbon_emissions_source(source_id: int, db: Session = Depends(get_db)):
    deleted_source = crud.delete_carbon_emissions_source(db=db, source_id=source_id)
    if deleted_source is None:
        raise HTTPException(status_code=404, detail="Carbon emissions source not found")
    return deleted_source


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
    db_emission_sources = crud.get_carbon_emissions_sources_by_id(db, source_id=footprint.source_id)
    if db_emission_sources is None:
        raise HTTPException(status_code=400, detail="Emissions source not found")
    
    return crud.create_carbon_footprint(db=db, footprint=footprint)

# Endpoint to update an existing carbon footprint entry
@app.put("/carbon_footprint/{footprint_id}", response_model=schemas.CarbonFootprint)
def update_carbon_footprint(
    footprint_id: int, footprint_update: schemas.CarbonFootprintUpdate, db: Session = Depends(get_db)
):
    updated_footprint = crud.update_carbon_footprint(db=db, footprint_id=footprint_id, footprint_update=footprint_update)
    if updated_footprint is None:
        raise HTTPException(status_code=404, detail="Carbon footprint not found")
    return updated_footprint

# Endpoint to delete a carbon footprint entry
@app.delete("/carbon_footprint/{footprint_id}", response_model=schemas.CarbonFootprint)
def delete_carbon_footprint(footprint_id: int, db: Session = Depends(get_db)):
    deleted_footprint = crud.delete_carbon_footprint(db=db, footprint_id=footprint_id)
    if deleted_footprint is None:
        raise HTTPException(status_code=404, detail="Carbon footprint not found")
    return deleted_footprint



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
    db_emissions_source = crud.get_emissions_source(db, emission_source_id=source_id)
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
    db_emission_sources = crud.get_carbon_emissions_sources_by_id(db, source_id=sequestration.source_id)
    if db_emission_sources is None:
        raise HTTPException(status_code=400, detail="Emissions source not found")
    
    return crud.create_carbon_sequestration(db=db, sequestration=sequestration)

@app.put("/carbon_sequestration/{seq_id}", response_model=schemas.CarbonSequestrationBase)
def update_carbon_sequestration(
    seq_id: int, seq_update: schemas.CarbonSequestrationUpdate, db: Session = Depends(get_db)
):
    updated_seq = crud.update_carbon_sequestration(db=db, seq_id=seq_id, seq_update=seq_update)
    if updated_seq is None:
        raise HTTPException(status_code=404, detail="Carbon sequestration entry not found")
    return updated_seq

# Endpoint to delete a carbon sequestration entry
@app.delete("/carbon_sequestration/{seq_id}", response_model=schemas.CarbonSequestrationBase)
def delete_carbon_sequestration(seq_id: int, db: Session = Depends(get_db)):
    deleted_seq = crud.delete_carbon_sequestration(db=db, seq_id=seq_id)
    if deleted_seq is None:
        raise HTTPException(status_code=404, detail="Carbon sequestration entry not found")
    return deleted_seq

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
    db_regulation = crud.get_regulation_by_name(db, regulation_name=regulation.regulation_name)
    if db_regulation:
        raise HTTPException(status_code=400, detail="Regulation already added")
    return crud.create_carbon_regulation(db=db, regulation=regulation)


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

@app.put("/regulation/{regulation_id}", response_model=schemas.CarbonRegulation)
def update_regulation(
    regulation_id: int, regulation_update: schemas.CarbonRegulationUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing regulation.

    Args:
        regulation_id (int): ID of the regulation to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.CarbonRegulation: The updated regulation.
    """
    updated_regulation = crud.update_regulation(db=db, regulation_id=regulation_id, regulation_update=regulation_update)
    if updated_regulation is None:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return updated_regulation


@app.delete("/regulation/{regulation_id}", response_model=schemas.CarbonRegulation)
def delete_regulation(regulation_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing regulation.

    Args:
        regulation_id (int): ID of the regulation to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.CarbonRegulation: The deleted regulation.
    """
    deleted_regulation = crud.delete_regulation(db=db, regulation_id=regulation_id)
    if deleted_regulation is None:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return deleted_regulation


app.include_router(router)