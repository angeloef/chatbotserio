---
name: search_properties
version: 1.0.0
description: Busca propiedades en Oberá según operación, tipo, zona, presupuesto y dormitorios.
ttl: permanent
category: search
security: read_only
---

# search_properties

## Summary (Level 1 — ~120 tokens, always loaded)
Busca propiedades inmobiliarias en Oberá con filtros por operación (alquiler/venta), tipo (departamento/casa/ph/terreno), zona (Centro/UNAM/Barrio Schuster/Ruta 14), presupuesto máximo en pesos y dormitorios mínimos. Todos los filtros son opcionales. Devuelve una lista formateada con IDs, precios, ubicación y características principales.

## Instructions (Level 2 — ~2K tokens, loaded when skill is relevant)

### Parámetros
- `operation` (opcional): "alquiler" o "venta". Si está vacío, busca en ambas.
- `tipo` (opcional): "departamento", "casa", "ph", "terreno". Acepta variantes: "depto"→"departamento", "casas"→"casa".
- `zona` (opcional): "Centro", "UNAM", "Barrio Schuster", "Ruta 14". Búsqueda parcial (ILIKE).
- `presupuesto_max` (opcional): monto máximo en ARS. 0 = sin límite.
- `dormitorios` (opcional): cantidad mínima de dormitorios. 0 = sin filtro.

### Comportamiento
- Si no hay resultados, sugiere ajustar filtros (subir presupuesto, ampliar zona, reducir dormitorios).
- El resultado incluye el ID entre corchetes para que el usuario pueda pedir detalles.
- Para alquileres muestra "$X/mes", para ventas muestra "$X".

### Ejemplos
- "busco depto alquiler Centro hasta 90 lucas" → operation=alquiler, tipo=departamento, zona=Centro, presupuesto_max=90000
- "quiero comprar casa en Schuster" → operation=venta, tipo=casa, zona=Barrio Schuster
- "busco terreno" → tipo=terreno (sin otros filtros, búsqueda amplia)

### Edge cases
- Si el usuario dice "departamentos" o "deptos", mapear a "departamento".
- Si no se especifica operación y los resultados mezclan alquiler/venta, mostrar ambos claramente etiquetados.
- Presupuesto en "lucas" = miles, "palos" o "millones" = millones.

## Implementation (Level 3 — loaded on execution)
Handler: `skills/search_properties/handler.py`
Schema: `skills/search_properties/schema.py`
Backend: SQLAlchemy async query sobre tabla `properties` en PostgreSQL.
