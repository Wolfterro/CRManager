from django.utils import timezone

from workalendar.america import Brazil


def get_working_days_from_date(date):
    now = timezone.now().date()
    cal = Brazil()

    return cal.get_working_days_delta(date, now)


def get_service_type_list():
    from manager.choices import SERVICE_CHOICES

    service_type_list = []
    for service in SERVICE_CHOICES:
        service_type_list.append({
            "value": service[0],
            "label": service[1]
        })

    return service_type_list
