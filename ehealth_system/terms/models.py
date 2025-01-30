from django.db import models

class TermsAndConditions(models.Model):
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Terms & Conditions (Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')})"
