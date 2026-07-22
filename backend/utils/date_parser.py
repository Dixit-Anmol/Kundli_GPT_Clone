"""
Robust Date and Time parsing helpers for API inputs.
"""
import datetime

def parse_time_str(time_str: str) -> datetime.time:
    """
    Parse a time string into a datetime.time object safely.
    Handles '%H:%M:%S', '%H:%M', '%I:%M %p', '%I:%M:%S %p', or raw colon splitting.
    """
    if not time_str:
        return datetime.time(12, 0, 0)
    time_str = str(time_str).strip()
    
    for fmt in ("%H:%M:%S", "%H:%M", "%I:%M %p", "%I:%M:%S %p", "%H:%M:%S.%f"):
        try:
            dt = datetime.datetime.strptime(time_str, fmt)
            return dt.time()
        except ValueError:
            pass

    # Fallback to manual colon splitting
    try:
        parts = time_str.split(":")
        h = int(parts[0]) if len(parts) > 0 else 12
        m = int(parts[1]) if len(parts) > 1 else 0
        s = int(float(parts[2])) if len(parts) > 2 else 0
        return datetime.time(h % 24, m % 60, s % 60)
    except Exception:
        return datetime.time(12, 0, 0)


def parse_date_str(date_str: str) -> datetime.date:
    """
    Parse a date string into a datetime.date object safely.
    Handles '%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', etc.
    """
    if not date_str:
        return datetime.date(2000, 1, 1)
    date_str = str(date_str).strip()

    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.date()
        except ValueError:
            pass

    try:
        parts = date_str.replace("/", "-").split("-")
        if len(parts) == 3:
            if len(parts[0]) == 4:
                return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
            else:
                return datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
    except Exception:
        pass
    return datetime.date(2000, 1, 1)
