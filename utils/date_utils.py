"""
Date and time utility functions.
"""
from datetime import datetime, timedelta, time
from typing import List, Tuple


def get_business_days(start_date: datetime, end_date: datetime) -> List[datetime]:
    """
    Get list of business days between start and end dates (excluding weekends).
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        List of business days
    """
    business_days = []
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 0-4 = Monday-Friday
            business_days.append(current_date)
        current_date += timedelta(days=1)
    
    return business_days


def calculate_training_dates(start_date: datetime, duration_weeks: int) -> Tuple[datetime, datetime]:
    """
    Calculate training end date based on start date and duration.
    
    Args:
        start_date: Training start date
        duration_weeks: Duration in weeks
    
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = start_date + timedelta(weeks=duration_weeks)
    return start_date, end_date


def get_next_training_day(current_date: datetime, skip_weekends: bool = True) -> datetime:
    """
    Get next training day (skip weekends if enabled).
    
    Args:
        current_date: Current date
        skip_weekends: Whether to skip weekends
    
    Returns:
        Next training day
    """
    next_day = current_date + timedelta(days=1)
    
    if skip_weekends:
        while next_day.weekday() >= 5:  # Skip Saturday and Sunday
            next_day += timedelta(days=1)
    
    return next_day


def create_datetime_with_time(date: datetime, hour: int, minute: int) -> datetime:
    """
    Create datetime with specific time.
    
    Args:
        date: Date part
        hour: Hour (0-23)
        minute: Minute (0-59)
    
    Returns:
        Datetime with specified time
    """
    return date.replace(hour=hour, minute=minute, second=0, microsecond=0)


def get_time_range(start_time: datetime, duration_minutes: int) -> Tuple[datetime, datetime]:
    """
    Get time range given start time and duration.
    
    Args:
        start_time: Start time
        duration_minutes: Duration in minutes
    
    Returns:
        Tuple of (start_time, end_time)
    """
    end_time = start_time + timedelta(minutes=duration_minutes)
    return start_time, end_time


def format_time_slot(start_time: datetime, end_time: datetime) -> str:
    """
    Format time slot as string.
    
    Args:
        start_time: Start time
        end_time: End time
    
    Returns:
        Formatted time slot string (e.g., "09:00 AM - 09:40 AM")
    """
    start_str = start_time.strftime("%I:%M %p")
    end_str = end_time.strftime("%I:%M %p")
    return f"{start_str} - {end_str}"
