from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import random
import argparse
from models import Base, Company, OffsetType, CarbonOffset, CompanyBranch, CarbonEmissionsSource, CarbonFootprint

def generate_data(num_companies, num_branches_per_company, num_offsets_per_company, num_emissions_per_branch, num_footprints_per_emission):

    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/dbproject')
    Session = sessionmaker(bind=engine)

    # shouldn't need this
    # Base.metadata.create_all(engine)

    session = Session()

    # Generate data
    for i in range(num_companies):
        company = Company(c_name=f"Company{i+1}")
        session.add(company)
        session.flush()

        for j in range(num_branches_per_company):
            branch = CompanyBranch(company_id=company.id, branch_name=f"Branch{j+1} of Company{i+1}")
            session.add(branch)
            session.flush()

            for k in range(num_emissions_per_branch):
                emission = CarbonEmissionsSource(branch_id=branch.id, source_type=f"Type{k+1}", total_emission_value=random.uniform(100.0, 1000.0))
                session.add(emission)
                session.flush()

                for l in range(num_footprints_per_emission):
                    footprint = CarbonFootprint(source_id=emission.id, footprint_value=random.uniform(10.0, 90.0))
                    session.add(footprint)

        for m in range(num_offsets_per_company):
            offset_type = random.choice(list(OffsetType))
            carbon_offset = CarbonOffset(company_id=company.id, offset_type=offset_type, offset_amount=random.randint(1000, 10000), date=datetime.date(2023, 1, 1))
            session.add(carbon_offset)

    # commit the transaction
    session.commit()

    session.close()

    print("Data has been added")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate test data for the database.")
    parser.add_argument('--companies', type=int, default=5, help='Number of companies to generate')
    parser.add_argument('--branches', type=int, default=2, help='Number of branches per company')
    parser.add_argument('--offsets', type=int, default=2, help='Number of carbon offsets per company')
    parser.add_argument('--emissions', type=int, default=3, help='Number of emissions sources per branch')
    parser.add_argument('--footprints', type=int, default=2, help='Number of carbon footprints per emission source')

    args = parser.parse_args()

    generate_data(args.companies, args.branches, args.offsets, args.emissions, args.footprints)
