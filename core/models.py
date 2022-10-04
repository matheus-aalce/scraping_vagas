from django.db import models


class TimeStampedModel(models.Model):
    """
    Classe abstrata para prover os campos created e modified.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
