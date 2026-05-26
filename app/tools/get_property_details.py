"""Get property details by ID."""

from typing import Any

from sqlalchemy import select

from app.core.database import async_session
from app.models.property import Property


async def get_property_details(property_id: int = 0) -> str:
    """Return full details for a specific property by its ID.

    Args:
        property_id: The numeric ID of the property (from search results).
    """
    if not property_id:
        return "Necesito el número de ID de la propiedad. Usá el número que aparece entre corchetes en los resultados de búsqueda, por ejemplo 'mostrame más del 3'."

    async with async_session() as session:
        result = await session.execute(
            select(Property).where(Property.id == property_id)
        )
        prop = result.scalars().first()

        if not prop:
            return f"No encontré ninguna propiedad con ID {property_id}. ¿Revisamos los resultados de búsqueda de nuevo?"

        op_label = "ALQUILER" if prop.operation == "alquiler" else "VENTA"
        price_str = (
            f"${prop.price:,.0f} por mes" if prop.operation == "alquiler"
            else f"${prop.price:,.0f}"
        )
        tipo_str = prop.property_type.capitalize()

        amenities_str = ", ".join(prop.amenities).replace("_", " ") if prop.amenities else "No especificados"

        return (
            f"🏠 {prop.title}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 ID: {prop.id} | {op_label}\n"
            f"📍 {prop.address}\n"
            f"🏘️  {tipo_str} en {prop.zone}, {prop.city}\n"
            f"💰 {price_str}\n"
            f"🛏️  {prop.bedrooms} dormitorio{'s' if prop.bedrooms != 1 else ''}"
            f"{' (monoambiente)' if prop.bedrooms == 0 else ''}\n"
            f"🚿 {prop.bathrooms} baño{'s' if prop.bathrooms != 1 else ''}\n"
            f"📐 {prop.covered_m2:.0f}m² cubiertos"
            f"{f' | {prop.total_m2:.0f}m² totales' if prop.total_m2 != prop.covered_m2 else ''}\n"
            f"✨ {', '.join(a.replace('_', ' ') for a in prop.amenities) if prop.amenities else 'No especificados'}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 {prop.description}"
        )
