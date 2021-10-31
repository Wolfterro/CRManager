from django.contrib import admin

from manager.models import CR, Activity, Process, PCE


# Register your models here.
# ==========================
@admin.register(CR)
class CRAdmin(admin.ModelAdmin):
    def activities_list(self, obj):
        return ", ".join([x.name for x in obj.activities.all()])
    activities_list.short_description = 'Atividades'

    list_display = ('number', 'user', 'rm', 'activities_list', 'expiration_date', )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    def entry_date_days_count(self, obj):
        return "{} / {}".format(obj.entry_date_days, obj.entry_date_working_days)
    entry_date_days_count.short_description = "Dias corridos / Dias úteis"

    def gru_compensation_days_count(self, obj):
        return "{} / {}".format(
            obj.gru_compensation_date_days if obj.gru_compensation_date_days else "-",
            obj.gru_compensation_date_working_days if obj.gru_compensation_date_working_days else "-"
        )
    gru_compensation_days_count.short_description = "Dias corridos / Dias úteis"

    list_display = (
        'protocol',
        'user',
        'service',
        'status',
        'entry_date',
        'entry_date_days_count',
        'gru_compensation_date',
        'gru_compensation_days_count',
        'om',
        'pce',
    )


@admin.register(PCE)
class PCEAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'pce_type', 'quantity', )
