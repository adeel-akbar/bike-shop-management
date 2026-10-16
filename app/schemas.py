from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BikeCreate(BaseModel):
    company: str
    model: str
    model_year: int
    registration_no: str | None = None
    engine_no: str
    chassis_no: str
    purchase_date: datetime | None = None
    purchase_price: int = Field(gt=0)
    seller_name: str
    seller_phone_no: str | None = None
    seller_cnic: str | None = None
    notes: str | None = None

class BikeResponse(BikeCreate):
    id: int
    status: bool
    purchase_date: datetime # type: ignore

    model_config = ConfigDict(from_attributes = True)

class BikeSale(BaseModel):
    buyer_name: str
    buyer_phone: str | None = None
    buyer_cnic: str | None = None
    sale_date: datetime | None = None
    sale_price: int = Field(gt=0)

class BikeSaleResponse(BikeSale):
    id: int
    bike_id: int
    receipt_no: int
    sale_date: datetime # type: ignore

    model_config = ConfigDict(from_attributes = True)