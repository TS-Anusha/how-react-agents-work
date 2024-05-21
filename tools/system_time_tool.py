import datetime
from langchain.agents import tool
import pytz

@tool
def check_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in the specified format"""

    # get the current date and time
    current_time = datetime.datetime.now()
    
    # format the time as a string in the format "YYYY-MM-DD HH:MM:SS"
    formatted_time = current_time.strftime(format)
    
    # return the formatted time
    return formatted_time

def get_current_utc_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current UTC time in the specified format"""
    # Get the current date and time in UTC
    current_utc_time = datetime.datetime.now(pytz.utc)

    return current_utc_time

@tool
def convert_time_zone(zone, format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current time converted to a particular time zone when provided the zone name which should be in this format "Region/City" """
    # Get the current date and time
    current_utc_time = get_current_utc_time()
    
    try:
        # Define the target time zone
        target_tz = pytz.timezone(zone)
    except pytz.UnknownTimeZoneError:
        all_time_zones = pytz.all_timezones

# Search for a specific time zone by partial name
        search_term = zone
       
        matching_zones = [zone for zone in all_time_zones if search_term in zone]
        if len(matching_zones)==0:
            return f"Not found even in the time zone list: {zone}"
        else:
            target_tz=pytz.timezone(matching_zones[0])
    
    # Convert the UTC time to the target time zone
    time_in_target_tz = current_utc_time.astimezone(target_tz)
    
    # Format the time as a string in the specified format
    formatted_time_in_tz = time_in_target_tz.strftime(format)
    
    # Return the formatted time in the target time zone
    return formatted_time_in_tz
