from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Bikes(Base):
    __tablename__= "bikes"
    id: Mapped[int] = mapped_column(primary_key = True,nullable = False)
    company: Mapped[str] = mapped_column(nullable = False)
    model: Mapped[str] = mapped_column(nullable = False)
    model_year: Mapped[int] = mapped_column(nullable = False)
    registration_no: Mapped[str | None] = mapped_column(nullable = True)
    engine_no: Mapped[str] = mapped_column(unique = True, nullable = False)
    chassis_no: Mapped[str] = mapped_column(unique = True, nullable = False)
    purchase_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone = True), 
                    server_default = func.now(), nullable = False)
    purchase_price: Mapped[int] = mapped_column(nullable = False)
    seller_name: Mapped[str] = mapped_column(nullable = False)
    seller_phone_no: Mapped[str | None] = mapped_column(nullable = True)
    seller_cnic: Mapped[str | None] = mapped_column(nullable = True)
    notes: Mapped[str | None] = mapped_column(nullable = True)
    status: Mapped[bool] = mapped_column(nullable = False, server_default = "true")
    sale_info: Mapped["Sales | None"] = relationship(back_populates = "bike_info")

class Sales(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(primary_key = True, nullable = False)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"),
                unique = True, nullable = False)
    buyer_name: Mapped[str] = mapped_column(nullable = False)
    buyer_phone: Mapped[str | None] = mapped_column(nullable = True)
    buyer_cnic: Mapped[str | None] = mapped_column(nullable = True)
    sale_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone = True),
                            server_default = func.now(), nullable = False)
    sale_price: Mapped[int] = mapped_column(nullable = False)
    bike_info: Mapped["Bikes"] = relationship(back_populates = "sale_info")