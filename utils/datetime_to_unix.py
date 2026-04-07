from datetime import datetime, timezone, timedelta

def datetime_to_unix_gmt8(datetime_str: str) -> int:
    # Define GMT+8 timezone
    gmt8 = timezone(timedelta(hours=8))
    
    # Parse input string
    dt = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
    
    # Attach GMT+8 timezone
    dt = dt.replace(tzinfo=gmt8)
    
    return int(dt.timestamp())

if __name__ == "__main__":
    print(datetime_to_unix_gmt8("10/03/2026 12:00:00"))
