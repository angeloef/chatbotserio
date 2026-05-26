"""Schedule a visit to view a property."""

async def schedule_visit(
    property_id: int = 0,
    nombre: str = "",
    telefono: str = "",
    dia: str = "",
    horario: str = "",
    consulta: str = "",
) -> str:
    """Register a visit request for a property."""
    if not property_id:
        return "Necesito saber qué propiedad querés visitar. ¿Cuál es el ID?"
    if not nombre:
        return "¿Me decís tu nombre completo para agendar la visita?"
    if not telefono:
        return "¿Me pasás tu número de teléfono o WhatsApp para confirmar?"
    
    lines = [
        "✅ ¡Visita agendada!",
        "",
        f"🏠 Propiedad: #{property_id}",
        f"👤 Nombre: {nombre}",
        f"📱 Teléfono: {telefono}",
    ]
    if dia:
        lines.append(f"📅 Día: {dia}")
    if horario:
        lines.append(f"🕐 Horario: {horario}")
    if consulta:
        lines.append(f"💬 Consulta: {consulta}")
    
    lines.append("")
    lines.append("Te vamos a confirmar por WhatsApp en las próximas 24-48 hs con la dirección exacta y horario coordinado. ¡Gracias!")
    
    return "\n".join(lines)
