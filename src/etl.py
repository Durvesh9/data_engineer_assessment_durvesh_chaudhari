import json
import re
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import session_factory, setup_database
from .models import (
    RawProperty, Property, Lead, Valuation, Hoa, Rehab, Tax
)
from pydantic import ValidationError, BaseModel

TABLE_MAP = {
    Property: "properties",
    Lead: "leads",
    Valuation: "valuations",
    Hoa: "hoa",
    Rehab: "rehab",
    Tax: "taxes"
}

def load_raw_data(filepath: str) -> list[dict]:
    """Loads raw data from a JSON file."""
    print(f"Loading raw data from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            data = json.loads(content)
        print(f"Loaded {len(data)} raw property records.")
        return data
    except FileNotFoundError:
        print(f"ERROR: Data file not found at {filepath}")
        print("Please ensure your 'fake_property_data_new.json' is in the 'data/' folder.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not decode JSON from {filepath}: {e}")
        exit(1)

def insert_data(session: Session, model_instance: BaseModel) -> int | None:
    """
    Inserts a Pydantic model instance into its corresponding table
    and returns the new primary key (ID).
    """
    table_name = TABLE_MAP.get(type(model_instance))
    if not table_name:
        raise TypeError(f"No table mapping found for model: {type(model_instance)}")

    data = model_instance.model_dump(exclude_unset=True)

    columns = ", ".join([f"`{col}`" for col in data.keys()])
    values = ", ".join([f":{col}" for col in data.keys()])

    sql = text(f"INSERT INTO `{table_name}` ({columns}) VALUES ({values})")

    try:
        result = session.execute(sql, data)
        session.flush()

        if result.lastrowid:
            return result.lastrowid
        return None

    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        print(f"Data: {data}")
        raise

def parse_sqft(sqft_str: str | None) -> int | None:
    """Parses strings like '5649 sqft' into integers."""
    if sqft_str is None:
        return None
    if isinstance(sqft_str, int):
        return sqft_str

    match = re.search(r'^\d+', str(sqft_str))
    if match:
        return int(match.group(0))
    return None

def process_and_load(session: Session, raw_data: list[dict]):
    """
    Validates, transforms, and loads data into the normalized database.
    """
    print("Starting data processing and loading...")
    property_count = 0
    valuation_count = 0
    rehab_count = 0
    hoa_count = 0
    tax_count = 0
    lead_count = 0

    for i, raw_record in enumerate(raw_data):
        try:
            raw_prop = RawProperty.model_validate(raw_record)

            prop_model = Property(
                property_title=raw_prop.Property_Title,
                address=raw_prop.Address,
                market=raw_prop.Market,
                flood=raw_prop.Flood,
                street_address=raw_prop.Street_Address,
                city=raw_prop.City,
                state=raw_prop.State,
                zip=raw_prop.Zip,
                property_type=raw_prop.Property_Type,
                highway=raw_prop.Highway,
                train=raw_prop.Train,
                tax_rate=raw_prop.Tax_Rate,
                sqft_basement=raw_prop.SQFT_Basement,
                htw=raw_prop.HTW,
                pool=raw_prop.Pool,
                commercial=raw_prop.Commercial,
                water=raw_prop.Water,
                sewage=raw_prop.Sewage,
                year_built=raw_prop.Year_Built,
                sqft_mu=raw_prop.SQFT_MU,
                sqft_total=parse_sqft(raw_prop.SQFT_Total),
                parking=raw_prop.Parking,
                bed=raw_prop.Bed,
                bath=raw_prop.Bath,
                basement_yes_no=raw_prop.BasementYesNo,
                layout=raw_prop.Layout,
                rent_restricted=raw_prop.Rent_Restricted,
                # FIX: Convert Neighborhood_Rating to string if it's not None
                neighborhood_rating=str(raw_prop.Neighborhood_Rating) if raw_prop.Neighborhood_Rating is not None else None,
                latitude=raw_prop.Latitude,
                longitude=raw_prop.Longitude,
                subdivision=raw_prop.Subdivision
            )

            new_property_id = insert_data(session, prop_model)
            if not new_property_id:
                raise Exception("Failed to get new property_id, skipping record.")

            property_count += 1

            lead_model = Lead(
                property_id=new_property_id,
                reviewed_status=raw_prop.Reviewed_Status,
                most_recent_status=raw_prop.Most_Recent_Status,
                source=raw_prop.Source,
                occupancy=raw_prop.Occupancy,
                net_yield=raw_prop.Net_Yield,
                irr=raw_prop.IRR,
                selling_reason=raw_prop.Selling_Reason,
                seller_type=raw_prop.Seller_Type
            )
            insert_data(session, lead_model)
            lead_count += 1

            for val_data in raw_prop.Valuation:
                val_model = Valuation(
                    property_id=new_property_id,
                    **val_data.model_dump()
                )
                insert_data(session, val_model)
                valuation_count += 1

            for hoa_data in raw_prop.HOA:
                hoa_model = Hoa.model_validate(
                    {"property_id": new_property_id, **hoa_data.model_dump()}
                )
                insert_data(session, hoa_model)
                hoa_count += 1

            for rehab_data in raw_prop.Rehab:
                rehab_model = Rehab.model_validate(
                    {"property_id": new_property_id, **rehab_data.model_dump()}
                )
                insert_data(session, rehab_model)
                rehab_count += 1

            if raw_prop.Taxes is not None:
                tax_model = Tax(
                    property_id=new_property_id,
                    taxes=raw_prop.Taxes
                )
                insert_data(session, tax_model)
                tax_count += 1

        except ValidationError as e:
            print(f"--- VALIDATION ERROR: Skipping record {i+1} (Title: {raw_record.get('Property_Title', 'N/A')}) ---")
            print(e)
            print("--------------------------------------------------")
            session.rollback()
        except Exception as e:
            print(f"--- RUNTIME ERROR: Skipping record {i+1} (Title: {raw_record.get('Property_Title', 'N/A')}) ---")
            print(f"Error: {e}")
            print("--------------------------------------------------")
            session.rollback()
            continue

    session.commit()
    print("\n--- ETL Process Complete ---")
    print(f"Successfully processed and loaded: {property_count} properties")
    print(f"Total leads loaded: {lead_count}")
    print(f"Total valuations loaded: {valuation_count}")
    print(f"Total rehab items loaded: {rehab_count}")
    print(f"Total HOA records loaded: {hoa_count}")
    print(f"Total tax records loaded: {tax_count}")

def main():
    print("=== Starting ETL Process ===")

    setup_database()

    raw_data = load_raw_data("data/fake_property_data_new.json")
    if not raw_data:
        print("No data to process. Exiting.")
        return

    session = session_factory()
    try:
        process_and_load(session, raw_data)
    except Exception as e:
        print(f"A fatal error occurred during the ETL process: {e}")
        session.rollback()
    finally:
        session.close()

    print("=== ETL Process Finished ===")

if __name__ == "__main__":
    main()
