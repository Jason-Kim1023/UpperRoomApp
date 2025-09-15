from datetime import date

def current_week_key(d: date | None = None) -> str:
    d = d or date.today()
    iso_year, iso_week, _ = d.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"
