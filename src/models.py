from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Any
from datetime import date
import re

# --- Pydantic Models for Raw Data Validation ---

class RawValuation(BaseModel):
    model_config = ConfigDict(extra='ignore')  # Ignore extra fields
    List_Price: Optional[float] = None
    Zestimate: Optional[float] = None
    Rent_Zestimate: Optional[float] = None
    High_FMR: Optional[float] = None
    Redfin_Value: Optional[float] = None
    Expected_Rent: Optional[float] = None
    Previous_Rent: Optional[float] = None
    ARV: Optional[float] = None
    Low_FMR: Optional[float] = None

class RawHOA(BaseModel):
    model_config = ConfigDict(extra='ignore')
    HOA: Optional[float] = None
    HOA_Flag: Optional[str] = None

class RawRehab(BaseModel):
    model_config = ConfigDict(extra='ignore')
    Underwriting_Rehab: Optional[float] = None
    Rehab_Calculation: Optional[float] = None
    Paint: Optional[str] = None
    Flooring_Flag: Optional[str] = None
    Foundation_Flag: Optional[str] = None
    Roof_Flag: Optional[str] = None
    HVAC_Flag: Optional[str] = None
    Kitchen_Flag: Optional[str] = None
    Bathroom_Flag: Optional[str] = None
    Appliances_Flag: Optional[str] = None
    Windows_Flag: Optional[str] = None
    Landscaping_Flag: Optional[str] = None
    Trashout_Flag: Optional[str] = None

class RawProperty(BaseModel):
    model_config = ConfigDict(extra='ignore')  # Ignore fields not defined

    # Fields from 'property' table
    Property_Title: str
    Address: str
    Market: Optional[str] = None
    Flood: Optional[str] = None
    Street_Address: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[str] = None
    Property_Type: Optional[str] = None
    Highway: Optional[str] = None
    Train: Optional[str] = None
    Tax_Rate: Optional[float] = None
    SQFT_Basement: Optional[int] = None
    HTW: Optional[str] = None
    Pool: Optional[str] = None
    Commercial: Optional[str] = None
    Water: Optional[str] = None
    Sewage: Optional[str] = None
    Year_Built: Optional[int] = None
    SQFT_MU: Optional[int] = None
    SQFT_Total: Optional[Any] = None  # Will parse this
    Parking: Optional[str] = None
    Bed: Optional[int] = None
    Bath: Optional[int] = None
    BasementYesNo: Optional[str] = None
    Layout: Optional[str] = None
    Rent_Restricted: Optional[str] = None
    Neighborhood_Rating: Optional[Any] = None  # <-- FIX: Accept int, str, or None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Subdivision: Optional[str] = None

    # Fields from 'Leads' table
    Reviewed_Status: Optional[str] = None
    Most_Recent_Status: Optional[str] = None
    Source: Optional[str] = None
    Occupancy: Optional[str] = None
    Net_Yield: Optional[float] = None
    IRR: Optional[float] = None
    Selling_Reason: Optional[str] = None
    Seller_Type: Optional[str] = None

    # Fields from 'Taxes' table
    Taxes: Optional[float] = None

    # Nested Lists
    Valuation: List[RawValuation]
    HOA: List[RawHOA]
    Rehab: List[RawRehab]

# --- Pydantic Models for Database Loading (Schema) ---

class Property(BaseModel):
    property_title: str
    address: str
    market: Optional[str] = None
    flood: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    property_type: Optional[str] = None
    highway: Optional[str] = None
    train: Optional[str] = None
    tax_rate: Optional[float] = None
    sqft_basement: Optional[int] = None
    htw: Optional[str] = None
    pool: Optional[str] = None
    commercial: Optional[str] = None
    water: Optional[str] = None
    sewage: Optional[str] = None
    year_built: Optional[int] = None
    sqft_mu: Optional[int] = None
    sqft_total: Optional[int] = None
    parking: Optional[str] = None
    bed: Optional[int] = None
    bath: Optional[int] = None
    basement_yes_no: Optional[str] = None
    layout: Optional[str] = None
    rent_restricted: Optional[str] = None
    neighborhood_rating: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    subdivision: Optional[str] = None

class Lead(BaseModel):
    property_id: int  # FK
    reviewed_status: Optional[str] = None
    most_recent_status: Optional[str] = None
    source: Optional[str] = None
    occupancy: Optional[str] = None
    net_yield: Optional[float] = None
    irr: Optional[float] = None
    selling_reason: Optional[str] = None
    seller_type: Optional[str] = None

class Valuation(BaseModel):
    property_id: int  # FK
    previous_rent: Optional[float] = Field(None, alias='Previous_Rent')
    list_price: Optional[float] = Field(None, alias='List_Price')
    zestimate: Optional[float] = Field(None, alias='Zestimate')
    arv: Optional[float] = Field(None, alias='ARV')
    expected_rent: Optional[float] = Field(None, alias='Expected_Rent')
    rent_zestimate: Optional[float] = Field(None, alias='Rent_Zestimate')
    low_fmr: Optional[float] = Field(None, alias='Low_FMR')
    high_fmr: Optional[float] = Field(None, alias='High_FMR')
    redfin_value: Optional[float] = Field(None, alias='Redfin_Value')

    class Config:
        populate_by_name = True  # Allow using aliases

class Hoa(BaseModel):
    property_id: int  # FK
    hoa_fee: Optional[float] = Field(None, alias='HOA')
    hoa_flag: Optional[str] = Field(None, alias='HOA_Flag')

    class Config:
        populate_by_name = True  # Allow using 'HOA' as alias

class Rehab(BaseModel):
    property_id: int  # FK
    underwriting_rehab: Optional[float] = Field(None, alias='Underwriting_Rehab')
    rehab_calculation: Optional[float] = Field(None, alias='Rehab_Calculation')
    paint: Optional[str] = Field(None, alias='Paint')
    flooring_flag: Optional[str] = Field(None, alias='Flooring_Flag')
    foundation_flag: Optional[str] = Field(None, alias='Foundation_Flag')
    roof_flag: Optional[str] = Field(None, alias='Roof_Flag')
    hvac_flag: Optional[str] = Field(None, alias='HVAC_Flag')
    kitchen_flag: Optional[str] = Field(None, alias='Kitchen_Flag')
    bathroom_flag: Optional[str] = Field(None, alias='Bathroom_Flag')
    appliances_flag: Optional[str] = Field(None, alias='Appliances_Flag')
    windows_flag: Optional[str] = Field(None, alias='Windows_Flag')
    landscaping_flag: Optional[str] = Field(None, alias='Landscaping_Flag')
    trashout_flag: Optional[str] = Field(None, alias='Trashout_Flag')

    class Config:
        populate_by_name = True

class Tax(BaseModel):
    property_id: int  # FK
    taxes: Optional[float] = None
