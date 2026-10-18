from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix = "/bikes",
    tags = ["bikes"],
    dependencies = [Depends(get_current_user)]
)

@router.post("/", response_model = schemas.BikeResponse, status_code=status.HTTP_201_CREATED)
def create_bike(bike: schemas.BikeCreate, db: Session = Depends(get_db)):  # noqa: B008
    new_bike = models.Bikes(**bike.model_dump(exclude_none=True))
    db.add(new_bike)
    db.commit() 
    db.refresh(new_bike)
    return new_bike


@router.get("/", response_model=list[schemas.BikeResponse])
def get_bikes(search: str = "", bike_status: bool | None = None,
    starting_date: date | None = None, ending_date: date | None = None,
              db:Session=Depends(get_db)):  # noqa: B008
    query = select(models.Bikes)

    if search:
        query = query.where(or_(
            models.Bikes.company.ilike(f"%{search}%"),
            models.Bikes.model.ilike(f"%{search}%"),
            models.Bikes.engine_no.ilike(f"%{search}%"),
            models.Bikes.registration_no.ilike(f"%{search}%"),
            models.Bikes.chassis_no.ilike(f"%{search}%")
        ))

    if bike_status is not None:
        query = query.where(
            models.Bikes.status.is_(bike_status)
        )

    if starting_date is not None and ending_date is not None and starting_date > ending_date:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Starting date cannot be after ending date"
            )

    if starting_date is not None:
        query = query.where(
          func.date(models.Bikes.purchase_date) >= starting_date  
        )
    if ending_date is not None:
        query = query.where(
            func.date(models.Bikes.purchase_date) <= ending_date
        )

    bikes = db.execute(query).scalars().all()

    return bikes


@router.get("/{id_of_bike}", response_model=schemas.BikeResponse)
def get_bike(id_of_bike: int, db: Session = Depends(get_db)):  # noqa: B008
    bike = db.execute(select(models.Bikes).where(models.Bikes.id == id_of_bike)).scalar_one_or_none()
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the bike with id{id_of_bike} is not present"

        )
    return bike

@router.patch("/{id_of_bike}", response_model=schemas.BikeResponse)
def update_bike(id_of_bike: int, bike: schemas.BikeUpdate, db: Session = Depends(get_db)):  # noqa: B008
    the_bike = db.execute(select(models.Bikes).where(models.Bikes.id == id_of_bike)).scalar_one_or_none()
    if not the_bike:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"the bike with id{id_of_bike} is not present"
        
                )
    update_data = bike.model_dump(exclude_unset=True)
    required_fields = {
        "company", "model", "model_year", "engine_no",
    "chassis_no", "purchase_date", "purchase_price",
    "seller_name"
    }
    for field in required_fields:
        if field in update_data and update_data[field] is None:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = f"{field} Field cannot be null"
            )
    for key, value in update_data.items():
        setattr(the_bike, key, value)
    db.commit()
    db.refresh(the_bike)
    return the_bike