from datetime import date

def current_week_key(d: date | None = None) -> str:
    d = d or date.today()
    iso_year, iso_week, _ = d.isocalendar()
    # Convert weekly ISO week to biweekly period
    # Each biweekly period covers 2 ISO weeks
    biweekly_period = ((iso_week - 1) // 2) + 1
    return f"{iso_year}-B{biweekly_period:02d}"
