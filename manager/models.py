from django.db import models
from django.utils import timezone

from manager.choices import RM_CHOICES, SERVICE_CHOICES, STATUS_CHOICES, GRU_STATUS_CHOICES, PCE_TYPE_CHOICES
from manager.utils import get_working_days_from_date


# Create your models here.
# ========================
class CR(models.Model):
    user = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, verbose_name="Usuário")

    number = models.CharField(max_length=16, default=None, verbose_name="Número do CR")
    expiration_date = models.DateField(default=None, verbose_name="Data de validade")
    rm = models.CharField(max_length=2, default=None, choices=RM_CHOICES, verbose_name="SFPC de vinculação (RM)")

    activities = models.ManyToManyField('manager.Activity', verbose_name="Atividades Autorizadas")

    class Meta:
        verbose_name = 'CR'
        verbose_name_plural = 'CRs'

    def __str__(self):
        return "{} - CR: {}".format(self.user.full_name, self.number)


class Activity(models.Model):
    name = models.CharField(max_length=100, default=None, verbose_name="Nome", unique=True)

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def __str__(self):
        return self.name


class Process(models.Model):
    user = models.ForeignKey('user.UserProfile', default=None, on_delete=models.CASCADE, verbose_name='Usuário')

    protocol = models.CharField(max_length=16, default=None, blank=True, null=True, verbose_name="Número de protocolo")
    entry_date = models.DateField(default=None, verbose_name="Data de entrada")
    service = models.CharField(max_length=100, default=None, choices=SERVICE_CHOICES, verbose_name="Serviço")
    status = models.CharField(max_length=16, default="pending", choices=STATUS_CHOICES, verbose_name="Situação do processo")
    reason = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="Motivo")
    om = models.CharField(max_length=100, default=None, verbose_name="OM")
    gru_status = models.CharField(max_length=10, default="pending", choices=GRU_STATUS_CHOICES, verbose_name="Situação da GRU")
    gru_compensation_date = models.DateField(default=None, blank=True, null=True, verbose_name="Data da compensação da GRU")

    pce = models.ForeignKey('manager.PCE', default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='PCE')

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'

    def __str__(self):
        return "{} - Nº {} ({})".format(self.get_service_display(), self.protocol, self.get_status_display())

    # Properties
    # ----------
    @property
    def service_label(self):
        return self.get_service_display()

    @property
    def status_label(self):
        return self.get_status_display()

    @property
    def gru_status_label(self):
        return self.get_gru_status_display()

    @property
    def entry_date_working_days(self):
        if self.entry_date:
            return get_working_days_from_date(self.entry_date)

        return None

    @property
    def entry_date_days(self):
        if self.entry_date:
            now = timezone.now().date()
            return (now - self.entry_date).days

        return None

    @property
    def gru_compensation_date_working_days(self):
        if self.gru_compensation_date:
            return get_working_days_from_date(self.gru_compensation_date)

        return None

    @property
    def gru_compensation_date_days(self):
        if self.gru_compensation_date:
            now = timezone.now().date()
            return (now - self.gru_compensation_date).days

        return None


class PCE(models.Model):
    name = models.CharField(max_length=200, default=None, verbose_name="Nome")
    manufacturer = models.CharField(max_length=200, default=None, verbose_name="Fabricante")
    pce_type = models.CharField(max_length=50, default=None, choices=PCE_TYPE_CHOICES, verbose_name="Tipo de PCE")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")

    class Meta:
        verbose_name = 'PCE'
        verbose_name_plural = 'PCEs'

    def __str__(self):
        return "{}x {} - {} ({})".format(str(self.quantity), self.name, self.manufacturer, self.get_pce_type_display())

    # Property
    @property
    def pce_type_label(self):
        return self.get_pce_type_display()
