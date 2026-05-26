---
name: get_property_details
version: 1.0.0
description: Muestra todos los detalles de una propiedad específica por su ID.
ttl: permanent
category: details
security: read_only
---

# get_property_details

## Summary (Level 1 — ~120 tokens)
Obtiene y formatea la ficha completa de una propiedad a partir de su ID numérico. Incluye: título, operación, tipo, zona, dirección, precio, dormitorios, baños, metros cuadrados, amenities y descripción. El ID se obtiene de los resultados de search_properties (número entre corchetes).

## Instructions (Level 2)
### Parámetros
- `property_id` (requerido): ID numérico de la propiedad.

### Formato de respuesta
Tarjeta estructurada con emojis:
```
🏠 Título
📋 ID: X | OPERACIÓN
📍 Dirección completa
🏘️ Tipo en Zona, Ciudad
💰 Precio (con "/mes" si es alquiler)
🛏️ N dormitorios
🚿 N baños
📐 Xm² cubiertos | Ym² totales
✨ Amenities
📝 Descripción completa
```

### Edge cases
- ID no encontrado → mensaje claro, sugerir volver a buscar.
- ID=0 o no especificado → pedir el número.

## Implementation (Level 3)
Handler: `skills/get_property_details/handler.py`
Schema: `skills/get_property_details/schema.py`
