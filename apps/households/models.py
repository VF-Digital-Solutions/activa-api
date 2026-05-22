from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.identity.models import User


class HouseholdNode(SoftDeleteModel):

    class Type(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        FAMILY = "FAMILY", "Familia"
        COMMUNITY = "COMMUNITY", "Comunidad"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=20, choices=Type.choices, default=Type.INDIVIDUAL
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    avatar_url = models.URLField(blank=True, null=True)
    address = models.JSONField(default=dict, blank=True)
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "households_node"
        verbose_name = "Nodo de hogar"
        verbose_name_plural = "Nodos de hogar"

    def __str__(self):
        return f"{self.name} ({self.type})"


class HouseholdMembership(TimeStampedModel):

    class Role(models.TextChoices):
        OWNER = "OWNER", "Propietario"
        ADMIN = "ADMIN", "Administrador"
        MEMBER = "MEMBER", "Miembro"
        GUEST = "GUEST", "Invitado"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    node = models.ForeignKey(
        HouseholdNode, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    nickname = models.CharField(max_length=50, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_invitations",
    )

    class Meta:
        db_table = "households_membership"
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"
        unique_together = [["user", "node"]]

    def __str__(self):
        return f"{self.user.email} — {self.node.name} ({self.role})"


class HouseholdInvitation(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        ACCEPTED = "ACCEPTED", "Aceptada"
        EXPIRED = "EXPIRED", "Expirada"
        REVOKED = "REVOKED", "Revocada"

    node = models.ForeignKey(
        HouseholdNode, on_delete=models.CASCADE, related_name="invitations"
    )
    invited_email = models.EmailField()
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invitations_sent"
    )
    role = models.CharField(max_length=10, choices=HouseholdMembership.Role.choices)
    token = models.UUIDField(unique=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "households_invitation"
        verbose_name = "Invitación"
        verbose_name_plural = "Invitaciones"

    def __str__(self):
        return f"{self.invited_email} → {self.node.name} ({self.status})"
