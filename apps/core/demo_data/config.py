"""Perfiles y rangos parametrizables para el seed de datos de demo.

Sin lógica de generación acá — solo los "puntos" ajustables que usan los
generadores en agenda.py / capitals.py / assessment.py.
"""

DEFAULT_SLEEP_HOURS = 8

# Cada tupla: (title, existential_category, energy_tag, duration_minutes,
# hour_start, probability_fulfilled). probability_fulfilled es la
# probabilidad de que el bloque termine en status FULFILLED (el resto se
# reparte entre OMITTED y, en el último día del rango, PLANNED).
WEEKDAY_BLOCK_PROFILE = [
    ("Trabajo enfocado", "OBLIGATIONS", "DRAINS", 180, 9, 0.85),
    ("Almuerzo", "INNER_NOURISHMENT", "NEUTRAL", 45, 13, 0.9),
    ("Reunión de equipo", "OBLIGATIONS", "DRAINS", 60, 15, 0.7),
    ("Ejercicio", "INNER_NOURISHMENT", "ENERGIZES", 45, 18, 0.6),
    ("Cena con pareja/familia", "BONDS", "ENERGIZES", 60, 20, 0.8),
    ("Lectura / meditación", "TRANSCENDENCE", "ENERGIZES", 30, 22, 0.5),
]

WEEKEND_BLOCK_PROFILE = [
    ("Dormir hasta tarde", "INNER_NOURISHMENT", "ENERGIZES", 60, 9, 0.9),
    ("Plan con amigos", "BONDS", "ENERGIZES", 120, 12, 0.75),
    ("Tareas del hogar", "OBLIGATIONS", "DRAINS", 90, 16, 0.6),
    ("Tiempo a solas / hobby", "TRANSCENDENCE", "ENERGIZES", 90, 19, 0.65),
]

EMOTION_POOL_POSITIVE = ["JOY", "GRATITUDE", "CALM", "LOVE", "PRIDE"]
EMOTION_POOL_NEGATIVE = [
    "SADNESS",
    "ANGER",
    "FEAR",
    "ANXIETY",
    "FRUSTRATION",
    "LONELINESS",
    "SHAME",
]

EMOTIONAL_LOG_NOTES_POSITIVE = [
    "Buen momento con la familia.",
    "Terminé una tarea pendiente, alivio.",
    "Charla linda con un amigo.",
    "Salió bien una reunión de trabajo.",
    "",
]
EMOTIONAL_LOG_NOTES_NEGATIVE = [
    "Mucha carga de trabajo hoy.",
    "Discusión que me dejó pensando.",
    "Cansancio acumulado.",
    "Preocupación por pendientes.",
    "",
]

# Plantillas de JournalEntry. Se interpolan con datos reales del día
# (categoría con más minutos en DRAINS, coherence_index) cuando el campo
# `{}` está presente.
JOURNAL_TEMPLATES_POSITIVE = {
    "energy_gain": [
        "Una charla con un amigo.",
        "Terminar mis tareas del día.",
        "El ejercicio de la mañana.",
        "Un momento de silencio.",
    ],
    "attention_needed": [
        "El descanso.",
        "La constancia con el ejercicio.",
        "La paciencia.",
        "El orden en las tareas.",
    ],
    "gratitude": [
        "La salud.",
        "El apoyo de la familia.",
        "Tener trabajo estable.",
        "Un día tranquilo.",
    ],
    "avoided_conversation": [
        "",
        "",
        "Poner un límite claro.",
    ],
}

JOURNAL_TEMPLATES_NEGATIVE = {
    "energy_drain": [
        "{top_drain_category} me drenó bastante hoy.",
        "Reuniones que se extendieron.",
        "Tráfico y traslados.",
        "Notificaciones constantes.",
    ],
    "attention_needed": [
        "Sentí que omití demasiado hoy (coherencia {coherence_index}).",
        "El descanso, estoy muy cansado.",
        "Bajar el ritmo.",
    ],
    "avoided_conversation": [
        "Hablar de un tema pendiente con un colega.",
        "Poner un límite claro que vengo postergando.",
        "",
    ],
    "gratitude": [
        "Haber llegado al final del día.",
        "El apoyo de la familia.",
        "La salud, a pesar de todo.",
    ],
}

# Score 1-10 por pregunta de assessment: interpolación lineal entre estos
# rangos según el progreso dentro del rango de fechas sembrado (day_index /
# total_days), + jitter aleatorio.
ASSESSMENT_SCORE_START_RANGE = (4, 6)
ASSESSMENT_SCORE_END_RANGE = (7, 9)
ASSESSMENT_SCORE_JITTER = 1

# Cada cuántos días (aprox) se siembra una nueva evaluación completa de cada
# tipo. El día 0 y el último día del rango siempre se siembran, para que el
# IVI pueda calcularse desde el primer día.
ASSESSMENT_SNAPSHOT_INTERVAL_DAYS = 7

# Proporción de minutos DRAINS sobre el total asignado a partir de la cual
# un día se considera "difícil" para efectos de derive_mood_bias.
MOOD_BIAS_DRAIN_THRESHOLD = 0.5
