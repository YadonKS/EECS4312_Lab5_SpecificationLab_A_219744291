## Student Name: YAdon Kassahun 
## Student ID: 219744291

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    # Convert time string "HH:MM" to minutes since midnight
    def time_to_minutes(time_str: str) -> int:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    # Convert minutes since midnight back to "HH:MM"
    def minutes_to_time(minutes: int) -> str:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    # Working hours: 9:00 to 17:00 (9*60 = 540 to 17*60 = 1020)
    # Lunch break: 12:00 to 13:00 (12*60 = 720 to 13*60 = 780)
    WORK_START = time_to_minutes("09:00")
    WORK_END = time_to_minutes("17:00")
    LUNCH_START = time_to_minutes("12:00")
    LUNCH_END = time_to_minutes("13:00")
    # Friday cutoff: meetings should not start after 15:00 on Fridays
    FRIDAY_CUTOFF = time_to_minutes("15:00")
    
    # Filter and sort events by start time
    sorted_events = sorted(events, key=lambda e: time_to_minutes(e["start"]))
    
    # Convert events to minutes for easier comparison
    event_times = [(time_to_minutes(e["start"]), time_to_minutes(e["end"])) for e in sorted_events]
    
    suggested_slots = []
    
    # Check time slots in 15-minute intervals
    current_time = WORK_START
    
    while current_time + meeting_duration <= WORK_END:
        # Skip lunch break
        if current_time >= LUNCH_START and current_time < LUNCH_END:
            current_time = LUNCH_END
            continue
        
        # Check if meeting would extend into or past lunch
        if current_time < LUNCH_START and current_time + meeting_duration > LUNCH_START:
            current_time = LUNCH_END
            continue
        
        # If Friday, skip slots that start after 15:00 (slots that start exactly at 15:00 are allowed)
        if isinstance(day, str) and day.strip().lower() == "fri" and current_time > FRIDAY_CUTOFF:
            current_time += 15
            continue
        
        # Check if this slot conflicts with any event
        slot_end = current_time + meeting_duration
        conflict = False
        
        for event_start, event_end in event_times:
            # Conflict if slot overlaps with event
            if current_time < event_end and slot_end > event_start:
                conflict = True
                break
            # Also skip if slot starts exactly at an event end time (no buffer)
            if current_time == event_end and current_time < LUNCH_START:
                conflict = True
                break
        
        if not conflict:
            suggested_slots.append(minutes_to_time(current_time))
        
        current_time += 15  # Move to next slot (15-min intervals)
        
    return suggested_slots