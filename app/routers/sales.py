from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix = "/sales",
    tags = ["sales"],
    dependencies = [Depends(get_current_user)]
)

@router.post("/", status_code = status.HTTP_201_CREATED, 
             response_model = schemas.BikeSaleResponse)
def bike_sale(bikesale: schemas.BikeSale, db: Session = Depends(get_db)):  # noqa: B008
    bike_sale_info = db.execute(select(models.Bikes).where(
        models.Bikes.id == bikesale.bike_id
    ).with_for_update()).scalar_one_or_none()
    if bike_sale_info is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"The bike with id:{bikesale.bike_id} is not present"
        ) 
    if not bike_sale_info.status:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"The bike with id:{bikesale.bike_id} is already sold"
        )
    new_sale = models.Sales(**bikesale.model_dump(exclude_none = True))
    db.add(new_sale)
    bike_sale_info.status = False
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Database constraint violation"
        )
    db.refresh(new_sale)
    return new_sale

@router.get("/", response_model = list[schemas.BikeSaleResponse])
def get_all_sales(db: Session = Depends(get_db)):  # noqa: B008
    all_sales = db.execute(select(models.Sales).options(selectinload(
        models.Sales.bike_info))).scalars().all()
    return all_sales

@router.get("/{sale_id}", response_model = schemas.BikeSaleResponse)
def get_one_sale(sale_id: int, db: Session = Depends(get_db)):  # noqa: B008
    sale = db.execute(select(models.Sales).where(models.Sales.id == sale_id)).scalar_one_or_none()
    if sale is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Sale with id: {sale_id} not found"
        )
    return sale