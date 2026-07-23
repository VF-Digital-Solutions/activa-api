from django.db import migrations

# Each indicator maps to the capital dimension it most directly measures.
HEALTH_SCALE_QUESTIONS = [
    (
        1,
        "TRANSCENDENTAL",
        "En una escala del 1 al 10, ¿qué tan claro tienes tu propósito o "
        "sentido de vida?",
    ),
    (
        2,
        "MORAL",
        "En una escala del 1 al 10, ¿qué tan coherente sientes que es tu "
        "vida entre lo que piensas, dices y haces?",
    ),
    (
        3,
        "STRENGTHS",
        "En una escala del 1 al 10, ¿qué tanta autonomía sientes para tomar "
        "tus propias decisiones?",
    ),
    (
        4,
        "RELATIONAL",
        "En una escala del 1 al 10, ¿qué tan alta es la calidad de tus "
        "relaciones más cercanas?",
    ),
    (
        5,
        "STRENGTHS",
        "En una escala del 1 al 10, ¿qué tan bien te recuperas frente a la "
        "adversidad o los contratiempos?",
    ),
    (
        6,
        "EMOTIONAL",
        "En una escala del 1 al 10, ¿qué tanta paz interior sientes en tu "
        "día a día?",
    ),
    (
        7,
        "EMOTIONAL",
        "En una escala del 1 al 10, ¿qué tan presente está la gratitud en "
        "tu vida cotidiana?",
    ),
    (
        8,
        "COGNITIVE",
        "En una escala del 1 al 10, ¿qué tan abierto estás a aprender y "
        "crecer, incluso cuando implica salir de tu zona de confort?",
    ),
    (
        9,
        "EMOTIONAL",
        "En una escala del 1 al 10, ¿qué tanto toleras la incomodidad o la "
        "incertidumbre sin evitarla?",
    ),
    (
        10,
        "COGNITIVE",
        "En una escala del 1 al 10, ¿qué tan estable y firme sientes tu "
        "identidad, independientemente de las circunstancias externas?",
    ),
]


def seed_health_scale(apps, schema_editor):
    Assessment = apps.get_model("assessment", "Assessment")
    Question = apps.get_model("assessment", "Question")

    assessment, _ = Assessment.objects.get_or_create(
        type="HEALTH_SCALE_10",
        version=1,
        defaults={
            "title": "Escala de salud existencial de 10 indicadores",
            "description": (
                "Diez indicadores de salud existencial: propósito, "
                "coherencia, autonomía, calidad de las relaciones, "
                "resiliencia, paz interior, gratitud, apertura al "
                "crecimiento, tolerancia al malestar e identidad estable."
            ),
        },
    )

    for order, capital_dimension, text in HEALTH_SCALE_QUESTIONS:
        Question.objects.get_or_create(
            assessment=assessment,
            order=order,
            defaults={
                "text": text,
                "capital_dimension": capital_dimension,
                "scale_type": "SCALE_1_10",
            },
        )


def unseed_health_scale(apps, schema_editor):
    Assessment = apps.get_model("assessment", "Assessment")
    Assessment.objects.filter(type="HEALTH_SCALE_10", version=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("assessment", "0002_seed_seven_area_audit"),
    ]

    operations = [
        migrations.RunPython(seed_health_scale, unseed_health_scale),
    ]
