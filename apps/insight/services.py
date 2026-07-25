from apps.assessment.models import Assessment, AssessmentResponse, AssessmentSnapshot
from apps.capitals.services import calculate_emotional_aggregates

# El indicador de "resiliencia" es la pregunta #5 de la escala de salud
# existencial de 10 indicadores (ver apps/assessment seed migration 0003).
# Si en el futuro se versiona esa evaluación y cambia el orden de las
# preguntas, este valor deberá actualizarse (o resolverse por texto/slug
# en vez de por orden).
RESILIENCE_QUESTION_ORDER = 5


def _latest_snapshot(user, assessment_type, as_of_date=None):
    queryset = AssessmentSnapshot.objects.filter(
        user=user, assessment__type=assessment_type
    )
    if as_of_date is not None:
        queryset = queryset.filter(snapshot_date__lte=as_of_date)
    return queryset.order_by("-snapshot_date", "-created_at").first()


def calculate_ivi(user, as_of_date=None):
    """Índice Vital Integrado: Assets - Liabilities + Adaptation.

    En el MVP, sin modelos dedicados a pasivos o capacidad de adaptación,
    ambos se derivan de la última evaluación de salud existencial (10
    indicadores):
      - Adaptation = puntaje del indicador de resiliencia.
      - Liabilities = 10 - promedio de todos los puntajes por dimensión de
        esa evaluación (a mayor salud existencial, menor pasivo).

    Assets = promedio de los puntajes por dimensión de la última auditoría
    de las siete áreas, salvo el capital emocional: si hay registros
    recientes en EmotionalLog (ventana de 7 días), se usa ese promedio de
    intensidad en su lugar.

    `as_of_date` recalcula el índice como si se hubiera evaluado en una
    fecha pasada (usado por el seed de datos de demo): restringe qué
    snapshots de evaluación y qué ventana emocional se consideran "ya
    conocidos" a esa fecha. Por defecto usa hoy, igual que antes.

    Retorna None si falta alguna de las dos evaluaciones base.
    """
    audit_snapshot = _latest_snapshot(user, Assessment.Type.AUDIT_7_AREAS, as_of_date)
    health_snapshot = _latest_snapshot(user, Assessment.Type.HEALTH_SCALE_10, as_of_date)

    if audit_snapshot is None or health_snapshot is None:
        return None

    assets_by_dimension = dict(audit_snapshot.scores_by_dimension)

    emotional_aggregate = calculate_emotional_aggregates(
        user, window_days=7, as_of_date=as_of_date
    )
    if emotional_aggregate["average_intensity"] is not None:
        assets_by_dimension["EMOTIONAL"] = emotional_aggregate["average_intensity"]

    assets = round(sum(assets_by_dimension.values()) / len(assets_by_dimension), 2)

    health_scores = list(health_snapshot.scores_by_dimension.values())
    liabilities = round(10 - (sum(health_scores) / len(health_scores)), 2)

    resilience_response = AssessmentResponse.objects.filter(
        attempt=health_snapshot.attempt, question__order=RESILIENCE_QUESTION_ORDER
    ).first()
    adaptation = resilience_response.score if resilience_response else 0

    ivi = round(assets - liabilities + adaptation, 2)

    return {
        "ivi": ivi,
        "assets": assets,
        "liabilities": liabilities,
        "adaptation": adaptation,
        "assets_by_dimension": assets_by_dimension,
    }
