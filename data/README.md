# 📊 Data — Maya Analytics

> Datos simulados (DUMMY) para el proyecto de análisis de conversaciones Maya.

## Archivos

### `maya_conversaciones.csv`
Base de datos de **100 conversaciones simuladas** con el asistente Maya de Banorte.

| Columna | Descripción |
|---------|-------------|
| conv_id | ID único de conversación |
| turno | Número de turno dentro de la conversación |
| fecha | Fecha del mensaje |
| hora | Hora del mensaje |
| canal | Canal de contacto (App Móvil, Web, WhatsApp, Teléfono) |
| texto_entrada | Mensaje del usuario |
| texto_salida | Respuesta de Maya |
| intencion_detectada | Intención clasificada por Watson |
| confianza_watson | Score de confianza (0-1) |
| sentimiento | positivo / neutro / negativo |
| csat_estimado | Satisfacción estimada (1-5) |
| transaccion_realizada | Tipo de transacción |
| resolucion | Resuelta / Abandonada |
| duracion_min | Duración en minutos |
| num_turnos_conv | Total de turnos en la conversación |

**Estadísticas:**
- 100 conversaciones · 434 mensajes totales
- 10 tipos de intención
- 4 canales de contacto

---
⚠️ **DUMMY DATA** — Generado por Yara (Banorte Claw) para simulación de hackathon
