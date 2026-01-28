import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

from apps.users.models import User


class Session(models.Model):
    """
    Модель сессии пользователя.
    Хранит JWT токен и позволяет инвалидировать сессии.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sessions'

    def __str__(self):
        return f"Session {self.id} for {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            from django.conf import settings
            hours = getattr(settings, 'JWT_EXPIRATION_HOURS', 24)
            self.expires_at = timezone.now() + timedelta(hours=hours)
        super().save(*args, **kwargs)

    @property
    def is_valid(self) -> bool:
        """Проверка валидности сессии."""
        return self.is_active and self.expires_at > timezone.now()

    def invalidate(self):
        """Инвалидировать сессию."""
        self.is_active = False
        self.save(update_fields=['is_active'])
