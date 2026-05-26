---
name: schedule_visit
version: 1.0.0
description: Coordina una visita para ver una propiedad seleccionada.
ttl: permanent
category: scheduling
security: read_write
---

# schedule_visit

## Summary (Level 1)
Permite agendar una visita a una propiedad. Recibe el ID de la propiedad, nombre, teléfono y horario preferido del interesado. Devuelve confirmación con los datos de la visita.

## Instructions (Level 2)
### Parámetros
- `property_id` (requerido): ID de la propiedad a visitar.
- `nombre` (requerido): Nombre completo del interesado.
- `telefono` (requerido): Número de contacto (WhatsApp).
- `dia` (opcional): Día preferido (formato libre).
- `horario` (opcional): Franja horaria preferida.

### Comportamiento
- Fase 1 (actual): registro local de la solicitud, mensaje de confirmación.
- Fase 2 (futuro): integración con Google Calendar para agendar automáticamente.
- Si falta información crítica (nombre, teléfono), solicitar antes de confirmar.

### Ejemplo
Usuario: "agendame para ver el depto 3, soy Juan, 3755-123456, el martes a las 11"
→ property_id=3, nombre="Juan", telefono="3755-123456", dia="martes", horario="11"

## Implementation (Level 3)
Handler: `skills/schedule_visit/handler.py`
Schema: `skills/schedule_visit/schema.py`
