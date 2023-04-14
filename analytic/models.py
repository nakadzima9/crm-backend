from django.db import models


class DeletionReason(models.Model):
    REASON_CHOICES = (
        (1, "причина1"),
        (2, "причина2"),
        (3, "причина3"),
        (4, "причина4"),
        (5, "причина5"),
        (6, "причина6"),
        (7, "причина7"),
        (8, "причина8"),
    )

    reason = models.PositiveSmallIntegerField(choices=REASON_CHOICES, verbose_name="Причина удаления")
    student_count = models.PositiveIntegerField(default=0, verbose_name="Количество удаленных студентов")

    def __str__(self):
        return f"{self.reason}: {self.student_count}"

    class Meta:
        verbose_name = "Причина удаления"
        verbose_name_plural = "Причины удаления"
