from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=140)
    details = models.TextField(blank=True)
    priority = models.IntegerField(default=1)  # 1..5
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
