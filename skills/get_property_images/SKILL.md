---
name: get_property_images
version: 1.0.0
description: Muestra las fotos disponibles de una propiedad por su ID.
ttl: permanent
category: details
security: read_only
---

# get_property_images

## Summary (Level 1)
Devuelve la lista de imágenes asociadas a una propiedad específica. Útil cuando el usuario pide ver fotos después de ver los detalles o resultados de búsqueda.

## Instructions (Level 2)
### Parámetros
- `property_id` (requerido): ID numérico de la propiedad.

### Comportamiento
- Si la propiedad no tiene imágenes: informa que aún no hay fotos cargadas.
- Si la propiedad no existe: informa y sugiere buscar de nuevo.

## Implementation (Level 3)
Handler: `skills/get_property_images/handler.py`
