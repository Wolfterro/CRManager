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
    list_display = ('protocol', 'user', 'service', 'status', 'entry_date', 'gru_compensation_date', 'om', 'pce', )


@admin.register(PCE)
class PCEAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'pce_type', 'quantity', )
