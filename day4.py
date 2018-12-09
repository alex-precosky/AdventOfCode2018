"""Advent of Code 2018: Day 4"""
from datetime import timedelta
from enum import Enum
import re
import dateutil.parser
import numpy as np


class EventType(Enum):
    WAKE_UP = 1,
    BEGIN_SHIFT = 2
    FALL_ASLEEP = 3

class Event:
    """Represents a guard arriving, falling asleep, or waking up.
    Aggrigated into Night objects"""

    UNKNOWN_GUARD_ID = -1

    def __init__(self, guard_id, date, minutes, event_type):
        self.guard_id = guard_id
        self.date = date
        self.minutes = minutes
        self.event_type = event_type

    def __eq__(self, other):
        if (self.guard_id == other.guard_id) and (self.date == other.date) and (self.minutes == other.minutes) and (self.event_type == other.event_type):
            return True
        else:
            return False

    def __repr__(self):
        return f'guard_id: {self.guard_id} date: {self.date} minutes: {self.minutes} event: {self.event_type}'

    @classmethod
    def from_string(self, event_str):

        guard_id_str = re.search(r'(?<=Guard #)\d+', event_str)
        guard_id = self.UNKNOWN_GUARD_ID

        if guard_id_str is not None:
            guard_id = int(guard_id_str.group(0))
            event_type = EventType.BEGIN_SHIFT
        elif event_str.find('wakes') != -1:
            event_type = EventType.WAKE_UP
        else:
            event_type = EventType.FALL_ASLEEP

        date_str = re.search(r'\d+-\d+-\d+', event_str).group(0)
        date = dateutil.parser.parse(date_str).date()

        hour_str = re.search(r'\d\d(?=\:)', event_str).group(0)
        hour = int(hour_str)

        minute_str = re.search(r'(?<=\:)\d\d', event_str).group(0)
        minute = int(minute_str)

        if hour == 23:
            minute = minute - 60
            date += timedelta(days=1)

        return Event(guard_id, date, minute, event_type)


class Night:
    """Each night has a date, and one guard that guards that night,
    and a list of events of them falling asleep and waking up"""

    def __init__(self, date):
        self.date = date
        self.guard_id = None
        self.sleep_wake_events = [] # list of events of sleep or awake, in the order in which they happened

    def populate_from_event(self, event):

        if event.event_type == EventType.BEGIN_SHIFT:
            self.guard_id = event.guard_id
            self.start_time = event.minutes

        elif event.event_type == EventType.FALL_ASLEEP or event.event_type == EventType.WAKE_UP:
            self.sleep_wake_events.append(event)
            self.sleep_wake_events = sorted(self.sleep_wake_events, key=lambda x: x.minutes)

        else:
            print("Tried to populate_from_event() for an invalid event type!")

    def minutes_asleep(self):
        """Counts up how many minute the guard spent asleep this night"""
        total = 0
            
        for i in range(0, len(self.sleep_wake_events), 2):
            if self.sleep_wake_events[i].event_type != EventType.FALL_ASLEEP or self.sleep_wake_events[i+1].event_type != EventType.WAKE_UP:
                print('Found a weird pattern of not sleeping before waking...')
                return 0
            else:
                total += self.sleep_wake_events[i+1].minutes - self.sleep_wake_events[i].minutes

                
        return total

    def guard_asleep_at_minute(self, minute):
        """Returns True if guard was asleep that night at specified minute"""
        for event in self.sleep_wake_events:
            if event.minutes > minute:
                return bool(event.event_type == EventType.WAKE_UP)

        return False

    def __repr__(self):
        return f'guard_id: {self.guard_id} sleep_wake_events: {self.sleep_wake_events}'


def find_guard_most_minutes_asleep(nights):
    guards = {} # key is guard id, value is minutes asleep
    max_guard = -1
    max_guard_minutes = -1

    for date, night in nights.items():

        if night.guard_id not in guards:
            guards[night.guard_id] = 0

        guards[night.guard_id] += night.minutes_asleep()

    for guard_id, minutes in guards.items():
        if minutes > max_guard_minutes:
            max_guard_minutes = minutes
            max_guard = guard_id

    return max_guard

def find_minute_guard_asleep_most(guard_id, nights):

    minutes = np.zeros(60)

    for minute in range(60):
        for date, night in nights.items():
            if night.guard_id == guard_id:
                if night.guard_asleep_at_minute(minute) is True:
                    minutes[minute] += 1

    max_minutes = max(minutes)
    for minute, count in enumerate(minutes):
        if count == max_minutes:
            return minute


# return guard, minute
def find_minute_guard_asleep_most_minutes(nights):

    max_nights = -1
    max_guard = -1
    max_minute = -1

    for minute in range(60):
        guards = {} # key is guard_id, value is nights asleep at that minute

        for date, night in nights.items():
            if night.guard_id not in guards and (night.guard_asleep_at_minute(minute)):
                guards[night.guard_id] = 0

            if night.guard_asleep_at_minute(minute):
                guards[night.guard_id] += 1
            
        # find which guard was asleep most this minute
        for guard_id, nights_asleep in guards.items():

            if nights_asleep > max_nights:
                max_nights = nights_asleep
                max_guard = guard_id
                max_minute = minute

    return max_guard, max_minute

def main():
    # key is date, value is night objects
    nights = {}

    for line in open('input/Day4.txt').readlines():
        event = Event.from_string(line.strip())

        if event.date not in nights:
            night = Night(event.date)
            nights[event.date] = night

        night = nights[event.date]
        night.populate_from_event(event)
        

    guard_id_asleep_most = find_guard_most_minutes_asleep(nights)
    print(f'Guard most asleep: {guard_id_asleep_most}')

    minutes_asleep = find_minute_guard_asleep_most(guard_id_asleep_most, nights)
    print(f'Asleep for {minutes_asleep} minutes')

    print(f'Part 1 product: {guard_id_asleep_most * minutes_asleep}')

    max_guard, max_minute = find_minute_guard_asleep_most_minutes(nights)

    print(f'Guard {max_guard} asleep the most on minute {max_minute}')
    print(f'Part 2 product: {max_guard * max_minute}')

if __name__ == "__main__":
    main()
