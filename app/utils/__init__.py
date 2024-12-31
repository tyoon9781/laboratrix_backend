from datetime import datetime, timezone

## datetime UTC
def utc_now():
    return datetime.now(tz=timezone.utc)