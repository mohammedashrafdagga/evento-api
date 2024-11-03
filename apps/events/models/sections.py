from django.db import models

from .events import Event


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey(Event, related_name="sections", on_delete=models.CASCADE)
    speaker = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "sections"
        verbose_name = "Section"
        verbose_name_plural = "Sections"
