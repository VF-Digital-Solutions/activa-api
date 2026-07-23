from django.db import migrations

AUDIT_QUESTIONS = [
    (
        1,
        "PHYSICAL",
        "En una escala del 1 al 10, ¿qué tan bien estás cuidando tu cuerpo "
        "(sueño, alimentación, ejercicio, salud física)?",
    ),
    (
        2,
        "EMOTIONAL",
        "En una escala del 1 al 10, ¿qué tan equilibrado te sientes "
        "emocionalmente en tu día a día?",
    ),
    (
        3,
        "RELATIONAL",
        "En una escala del 1 al 10, ¿qué tan satisfecho estás con la calidad "
        "de tus vínculos y relaciones cercanas?",
    ),
    (
        4,
        "COGNITIVE",
        "En una escala del 1 al 10, ¿qué tanto estás nutriendo tu mente "
        "(aprendizaje, curiosidad, claridad mental)?",
    ),
    (
        5,
        "MORAL",
        "En una escala del 1 al 10, ¿qué tan alineadas sientes tus acciones "
        "diarias con tus valores y principios?",
    ),
    (
        6,
        "TRANSCENDENTAL",
        "En una escala del 1 al 10, ¿qué tan conectado te sientes con un "
        "propósito o sentido más allá de lo inmediato?",
    ),
    (
        7,
        "STRENGTHS",
        "En una escala del 1 al 10, ¿qué tanto estás utilizando y "
        "desarrollando tus fortalezas y talentos personales?",
    ),
]


def seed_audit(apps, schema_editor):
    Assessment = apps.get_model("assessment", "Assessment")
    Question = apps.get_model("assessment", "Question")

    assessment, _ = Assessment.objects.get_or_create(
        type="AUDIT_7_AREAS",
        version=1,
        defaults={
            "title": "Auditoría de las siete áreas",
            "description": (
                "Diagnóstico rápido del patrimonio existencial: una pregunta "
                "por cada uno de los siete capitales (físico, emocional, "
                "relacional, cognitivo, moral, trascendental, fortalezas)."
            ),
        },
    )

    for order, capital_dimension, text in AUDIT_QUESTIONS:
        Question.objects.get_or_create(
            assessment=assessment,
            order=order,
            defaults={
                "text": text,
                "capital_dimension": capital_dimension,
                "scale_type": "SCALE_1_10",
            },
        )


def unseed_audit(apps, schema_editor):
    Assessment = apps.get_model("assessment", "Assessment")
    Assessment.objects.filter(type="AUDIT_7_AREAS", version=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("assessment", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_audit, unseed_audit),
    ]
