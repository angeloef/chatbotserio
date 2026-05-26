---
name: get_faq_answer
version: 1.0.0
description: Responde preguntas frecuentes sobre alquiler, compra, requisitos y procesos.
ttl: permanent
category: knowledge
security: read_only
---

# get_faq_answer

## Summary (Level 1)
Responde preguntas frecuentes sobre el proceso inmobiliario en Oberá: requisitos para alquilar, tipos de garantía, duración de contratos, política de mascotas, coordinación de visitas, zonas disponibles, precios de referencia y datos de contacto.

## Instructions (Level 2)
### Parámetros
- `pregunta` (requerido): texto de la pregunta o keyword del tema.

### Temas cubiertos
- `requisitos`: Documentación necesaria (DNI, recibos, garantía, depósito)
- `garantía`: Tipos aceptados (propietaria en Oberá o recibo 3x)
- `contrato`: Duración 24 meses, ajuste IPC, comisión 4%
- `mascotas`: Política general (departamentos no, casas con patio sí)
- `visita` / `agendar`: Proceso de coordinación (24-48hs, datos necesarios)
- `zonas`: Las 4 zonas de Oberá con descripciones
- `precios`: Rangos actualizados por tipo y operación
- `servicios`: Agua, electricidad, gas natural/envasado
- `contacto`: WhatsApp, email, oficina, horarios

### Edge cases
- Pregunta no reconocida → ofrecer lista de temas disponibles.
- Matching difuso: busca keywords en la pregunta para mapear al tema correcto.

## Implementation (Level 3)
Handler: `skills/get_faq_answer/handler.py`
Backend: Diccionario estático con 11 entradas FAQ.
