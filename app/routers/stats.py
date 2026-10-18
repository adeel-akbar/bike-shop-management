from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix = "/stats",
    tags = ["stats"],
    dependencies = [Depends(get_current_user)]
)

@router.get("/")
def get_stats(db: Session = Depends(get_db)):  # noqa: B008

    query = select(func.count(models.Bikes.id))

    no_of_bikes = db.execute(query).scalar_one()
    available_bikes = db.execute(query.where(models.Bikes.status.is_(True))).scalar_one()
    sold_bikes = db.execute(query.where(models.Bikes.status.is_(False))).scalar_one()
    total_purchase_cost = db.execute(select(func.coalesce(func.sum(models.Bikes.purchase_price), 0))).scalar_one()
    inventory_cost = db.execute(select(func.coalesce(func.sum(models.Bikes.purchase_price), 0)).where(
        models.Bikes.status.is_(True)
    )).scalar_one()
    total_sales_revenue = db.execute(select(func.coalesce(func.sum(models.Sales.sale_price), 0))).scalar_one()
    total_profit = db.execute(select(
        func.coalesce(func.sum(
            models.Sales.sale_price - models.Bikes.purchase_price), 0)
            ).select_from(models.Sales)
            .join(models.Bikes, models.Sales.bike_id == models.Bikes.id)).scalar_one()

    return {"total_bikes": no_of_bikes, 
            "available_bikes": available_bikes, 
            "sold_bikes": sold_bikes,
            "total_purchase_cost": total_purchase_cost,
            "inventory_cost": inventory_cost,
            "total_sales_revenue": total_sales_revenue,
            "total_profit": total_profit
            }
