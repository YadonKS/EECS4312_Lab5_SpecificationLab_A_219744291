## Student Name:
## Student ID: 

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots


def test_regular_day_with_three_meetings():
    """
    Test case 1: Scheduling on a regular day with 3 meetings already in the list.
    Verifies that available slots are correctly identified around multiple meetings.
    """
    events = [
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
        {"start": "14:00", "end": "15:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    
    # Verify meetings block their time slots
    assert "09:30" not in slots
    assert "10:00" not in slots  # Back-to-back prevention
    assert "11:00" not in slots
    assert "14:00" not in slots
    
    # Verify available slots exist
    assert "09:00" in slots  # Before first meeting
    assert "10:15" in slots  # Between first and second meeting
    assert "13:00" in slots  # Between second and third meeting
    assert "15:00" in slots  # After third meeting (back-to-back prevention only applies during work hours before lunch)
    assert "15:15" in slots  # After third meeting


def test_no_available_slots():
    """
    Test case 2: A day with no available slots (fully booked).
    All time slots are occupied by meetings.
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "17:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    
    # No slots should be available (lunch bridge is too short for 30-min meeting)
    assert len(slots) == 0


def test_all_slots_available():
    """
    Test case 3: A day with all slots available (no meetings scheduled).
    Verifies that all valid time slots throughout the day are suggested.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    
    # Morning slots
    assert "09:00" in slots
    assert "09:15" in slots
    assert "09:30" in slots
    
    # Before lunch
    assert "11:30" in slots
    
    # Lunch should not be available
    assert "12:00" not in slots
    assert "12:30" not in slots
    
    # After lunch
    assert "13:00" in slots
    assert "15:00" in slots
    
    # Late afternoon
    assert "16:30" in slots
    
    # Last possible slot for 30-min meeting
    assert "16:45" not in slots  # Would end at 17:15, past work hours


def test_only_one_slot_available():
    """
    Test case 4: A heavily booked day with only one available slot.
    Verifies that a single available slot is correctly identified.
    """
    events = [
        {"start": "09:00", "end": "09:30"},
        {"start": "09:45", "end": "12:00"},
        {"start": "13:00", "end": "16:30"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    
    # Only 16:30-17:00 should be available for a 30-minute meeting
    assert len(slots) == 1
    assert slots[0] == "16:30"


def test_single_slot_at_three_pm_two_hour_meeting():
    """
    Test case 5: Only one slot available at 3pm with a 2-hour meeting duration.
    The meeting should start at 15:00 (3pm) and end at 17:00 (5pm, end of work day).
    """
    events = [
        {"start": "09:00", "end": "12:00"},
        {"start": "13:00", "end": "15:00"},
    ]
    slots = suggest_slots(events, meeting_duration=120, day="2026-02-01")  # 120 min = 2 hours
    
    # Only 15:00-17:00 should work for a 2-hour meeting
    assert len(slots) == 1
    assert slots[0] == "15:00"
    
    # Verify no other slots are available
    assert "14:00" not in slots  # Back-to-back prevention
    assert "14:30" not in slots  # Insufficient gap before end of day

"""TODO: Add at least 5 additional test cases to test your implementation."""
