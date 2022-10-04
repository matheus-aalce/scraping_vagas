import uuid

from django.db import models

from core.models import TimeStampedModel


class Vaga(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ubs = models.CharField("UBS", max_length=255, null=True, blank=True)
    endereco = models.CharField("Endereço", max_length=255, null=True, blank=True)
    carga_horaria = models.CharField(
        "Carga horária", max_length=255, null=True, blank=True
    )
    salario_base = models.CharField(
        "Salário base", max_length=255, null=True, blank=True
    )
    beneficios = models.TextField("Benefícios", null=True, blank=True)
    especialidades = models.CharField(
        "Especialidades", max_length=255, null=True, blank=True
    )
    fonte = models.CharField("Fonte", max_length=255, null=True, blank=True)

    def __str__(self):
        if self.ubs:
            return self.ubs
        return str(self.id)

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
        ordering = ["-modified", "-created"]
