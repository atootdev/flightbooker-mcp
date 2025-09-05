from datetime import datetime

def validate_date(date_str: str, field_name: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")  # just validates format
        return date_str  # keep as string
    except ValueError:
        raise ValueError(
            f"Invalid {field_name} '{date_str}'. Must be in YYYY-MM-DD format."
        )