from rest_framework import serializers

from apps.assessment.models import (
    Assessment,
    AssessmentAttempt,
    AssessmentResponse,
    AssessmentSnapshot,
    Question,
)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "order", "text", "capital_dimension", "scale_type"]


class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = [
            "id",
            "type",
            "version",
            "title",
            "description",
            "questions",
        ]


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    assessment = AssessmentSerializer(read_only=True)

    class Meta:
        model = AssessmentAttempt
        fields = [
            "id",
            "assessment",
            "status",
            "created_at",
            "completed_at",
        ]
        read_only_fields = fields


class StartAssessmentSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Assessment.Type.choices)

    def validate_type(self, value):
        assessment = (
            Assessment.objects.filter(type=value).order_by("-version").first()
        )
        if assessment is None:
            raise serializers.ValidationError(
                "No existe una evaluación publicada para este tipo."
            )
        self.assessment = assessment
        return value


class AnswerSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate_question(self, question):
        attempt = self.context["attempt"]
        if question.assessment_id != attempt.assessment_id:
            raise serializers.ValidationError(
                "La pregunta no pertenece a la evaluación de este intento."
            )
        return question


class AssessmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResponse
        fields = ["id", "question", "score", "created_at"]
        read_only_fields = fields


class AssessmentSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentSnapshot
        fields = ["id", "attempt", "snapshot_date", "scores_by_dimension"]
        read_only_fields = fields
