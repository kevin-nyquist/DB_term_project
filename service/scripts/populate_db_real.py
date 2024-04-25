from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import random
import argparse
from app.models.models import Base, Company, OffsetType, CarbonOffset, CompanyBranch, CarbonEmissionsSource, CarbonFootprint, CarbonSequestration

# Example lists for generating company names
prefixes = ["Enviro", "Green", "Eco", "Bio", "Planet", "Sustain", "Terra", "Vita", "Geo", "Orga"]
suffixes = ["Tech", "Solutions", "World", "Life", "Savers", "Innovators", "Guardians", "Pioneers", "Advocates", "Stewards"]

branch_descriptors = ["North", "South", "East", "West", "Central"]
source_types = ["Factory Emission", "Vehicle Emission", "Agricultural Emission", "Residential Emission"]

def generate_company_name():
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    return f"{prefix}{suffix}"

def generate_data(num_companies, num_branches_per_company, num_offsets_per_company, num_emissions_per_branch, num_footprints_per_emission, num_sequestrations_per_emission):
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/dbproject')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Generate data
    for i in range(num_companies):
        company_name = generate_company_name()
        company = Company(c_name=company_name)
        session.add(company)
        session.flush()

        for j in range(num_branches_per_company):
            branch_name = f"{branch_descriptors[j % len(branch_descriptors)]} Branch of {company_name}"
            branch = CompanyBranch(company_id=company.id, branch_name=branch_name)
            session.add(branch)
            session.flush()

            for k in range(num_emissions_per_branch):
                source_type = random.choice(source_types)
                emission = CarbonEmissionsSource(branch_id=branch.id, source_type=source_type, total_emission_value=random.uniform(100.0, 1000.0))
                session.add(emission)
                session.flush()

                for l in range(num_footprints_per_emission):
                    footprint = CarbonFootprint(source_id=emission.id, footprint_value=random.uniform(10.0, 90.0))
                    session.add(footprint)

                for m in range(num_sequestrations_per_emission):
                    sequestration = CarbonSequestration(source_id=emission.id, seq_value=random.uniform(10.0, 90.0))
                    session.add(sequestration)

        for n in range(num_offsets_per_company):
            offset_type = random.choice(list(OffsetType))
            carbon_offset = CarbonOffset(company_id=company.id, offset_type=offset_type, offset_amount=random.randint(1000, 10000), date=datetime.date(2023, 1, 1))
            session.add(carbon_offset)

    # commit the transaction
    session.commit()
    session.close()

    print("Data has been added")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate test data for the database.")
    parser.add_argument('--companies', type=int, default=10, help='Number of companies to generate')
    parser.add_argument('--branches', type=int, default=2, help='Number of branches per company')
    parser.add_argument('--offsets', type=int, default=2, help='Number of carbon offsets per company')
    parser.add_argument('--emissions', type=int, default=3, help='Number of emissions sources per branch')
    parser.add_argument('--footprints', type=int, default=2, help='Number of carbon footprints per emission source')
    parser.add_argument('--sequestrations', type=int, default=2, help='Number of carbon sequestrations per emission source')
    args = parser.parse_args()

    generate_data(args.companies, args.branches, args.offsets, args.emissions, args.footprints, args.sequestrations)