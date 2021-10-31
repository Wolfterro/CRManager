from django.utils import timezone

from workalendar.america import Brazil


def get_working_days_from_date(date):
    now = timezone.now().date()
    cal = Brazil()

    return cal.get_working_days_delta(date, now)
