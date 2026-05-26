---
name: compare_properties
version: 1.0.0
description: Compara dos o más propiedades lado a lado.
ttl: permanent
category: search
security: read_only
---

# compare_properties

## Summary (Level 1)
Permite comparar hasta 3 propiedades simultáneamente, mostrando una tabla comparativa con precio, metros, dormitorios, amenities y ubicación. Ideal cuando el usuario duda entre opciones.

## Instructions (Level 2)
### Parámetros
- `property_ids` (requerido): lista de IDs a comparar (máximo 3).

### Formato
Tabla comparativa:
```
           | Prop A     | Prop B     | Prop C
Precio     | $85.000/m  | $55.000/m  | $120.000/m
m²         | 45         | 30         | 65
Dormitorios| 1          | 0          | 2
Zona       | Centro     | Centro     | Centro
Amenities  | agua, gas  | electric.  | agua, gas, balcón
```

### Edge cases
- Si algún ID no existe, mostrar los que sí existen con un aviso.
- Si solo se pasa 1 ID, sugerir usar get_property_details en su lugar.

## Implementation (Level 3)
Handler: `skills/compare_properties/handler.py`
