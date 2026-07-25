import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.agenda.services import calculate_coherence_index, calculate_daily_distribution
from apps.assessment.models import Assessment
from apps.core.demo_data.agenda import generate_time_blocks_for_day
from apps.core.demo_data.assessment import is_assessment_day, seed_assessment_snapshot
from apps.core.demo_data.capitals import (
    derive_mood_bias,
    generate_emotional_logs_for_day,
    generate_journal_entry_for_day,
)
from apps.core.demo_data.cleanup import delete_existing_range
from apps.core.demo_data.config import DEFAULT_SLEEP_HOURS
from apps.core.demo_data.insight import seed_ivi_snapshot_for_day

User = get_user_model()

MIN_WEEKS = 1
MAX_WEEKS = 8


class Command(BaseCommand):
    help = (
        "Siembra datos de demo (agenda, emociones, diario, evaluaciones e IVI) "
        "para un usuario existente, reutilizando la lógica real de negocio "
        "(calculate_ivi, calculate_daily_distribution, calculate_coherence_index) "
        "en vez de generar valores independientes al azar. Idempotente: borra "
        "primero el mismo rango de fechas del usuario antes de sembrar.\n\n"
        "El rango de fechas siempre termina hoy (timezone.localdate()); con el "
        "mismo --seed, correrlo el mismo día produce el mismo dataset."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--user", required=True, help="username o email del usuario a sembrar"
        )
        parser.add_argument(
            "--weeks",
            type=int,
            default=2,
            help=f"cantidad de semanas a sembrar ({MIN_WEEKS}-{MAX_WEEKS}, default 2)",
        )
        parser.add_argument(
            "--seed", type=int, default=42, help="semilla para reproducibilidad"
        )

    def handle(self, *args, **options):
        user = self._resolve_user(options["user"])
        weeks = self._validate_weeks(options["weeks"])
        rng = random.Random(options["seed"])

        if not Assessment.objects.filter(type=Assessment.Type.AUDIT_7_AREAS).exists() or (
            not Assessment.objects.filter(type=Assessment.Type.HEALTH_SCALE_10).exists()
        ):
            raise CommandError(
                "Faltan las plantillas de evaluación base (AUDIT_7_AREAS / "
                "HEALTH_SCALE_10). Corré las migraciones de apps.assessment."
            )

        total_days = weeks * 7
        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=total_days - 1)

        with transaction.atomic():
            delete_existing_range(user, start_date, end_date)

            for day_index in range(total_days):
                date = start_date + timedelta(days=day_index)
                is_last_day = day_index == total_days - 1

                generate_time_blocks_for_day(user, date, rng, allow_planned=is_last_day)

                distribution = calculate_daily_distribution(
                    user, date, sleep_hours=DEFAULT_SLEEP_HOURS
                )
                coherence = calculate_coherence_index(user, date)
                mood_bias = derive_mood_bias(distribution, coherence)

                generate_emotional_logs_for_day(user, date, rng, mood_bias)
                generate_journal_entry_for_day(
                    user, date, rng, mood_bias, distribution, coherence
                )

                if is_assessment_day(day_index, total_days):
                    seed_assessment_snapshot(
                        user, date, Assessment.Type.AUDIT_7_AREAS, day_index, total_days, rng
                    )
                    seed_assessment_snapshot(
                        user, date, Assessment.Type.HEALTH_SCALE_10, day_index, total_days, rng
                    )

                seed_ivi_snapshot_for_day(user, date)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completo para {user} — {total_days} días "
                f"({start_date} a {end_date})."
            )
        )

    def _resolve_user(self, identifier):
        user = User.objects.filter(username=identifier).first() or User.objects.filter(
            email=identifier
        ).first()
        if user is None:
            raise CommandError(f"No existe un usuario con username/email '{identifier}'")
        return user

    def _validate_weeks(self, weeks):
        if not MIN_WEEKS <= weeks <= MAX_WEEKS:
            raise CommandError(f"--weeks debe estar entre {MIN_WEEKS} y {MAX_WEEKS}")
        return weeks
