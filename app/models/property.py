"""Property model — matches InmuebleBot Oberá seed pattern."""

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Property(Base):
    """Real estate property in Oberá."""

    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    operation: Mapped[str] = mapped_column(String(20), nullable=False)  # alquiler / venta
    property_type: Mapped[str] = mapped_column(String(30), nullable=False)  # departamento, casa, ph, terreno
    zone: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), default="Oberá")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(5), default="ARS")
    bedrooms: Mapped[int] = mapped_column(Integer, default=1)
    bathrooms: Mapped[int] = mapped_column(Integer, default=1)
    covered_m2: Mapped[float] = mapped_column(Float, default=0)
    total_m2: Mapped[float] = mapped_column(Float, default=0)
    description: Mapped[str] = mapped_column(String(1000), default="")
    address: Mapped[str] = mapped_column(String(200), default="")
    images: Mapped[list[str]] = mapped_column(JSON, default=list)
    amenities: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serializable representation for agent responses."""
        return {
            "id": self.id,
            "title": self.title,
            "operation": self.operation,
            "tipo": self.property_type,
            "zona": self.zone,
            "ciudad": self.city,
            "precio": self.price,
            "moneda": self.currency,
            "dormitorios": self.bedrooms,
            "baños": self.bathrooms,
            "m2_cubiertos": self.covered_m2,
            "m2_totales": self.total_m2,
            "descripcion": self.description,
            "direccion": self.address,
            "imagenes": len(self.images),
            "amenities": self.amenities,
        }
