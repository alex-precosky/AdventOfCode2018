from datetime import datetime
import dateutil.parser
import unittest
from day4 import Event, EventType

class Test(unittest.TestCase):

    def test_parse_wakeup(self):
        target = '[1518-11-22 00:49] wakes up'
        expected = Event(guard_id = Event.UNKNOWN_GUARD_ID,
                         date = dateutil.parser.parse('1518-11-22').date(),
                         minutes = 49,
                         event_type = EventType.WAKE_UP)

        actual = Event.from_string(target)
        assert expected == actual

    def test_parse_sleep(self):
        target = '[1518-11-22 00:49] falls asleep'
        expected = Event(guard_id = Event.UNKNOWN_GUARD_ID,
                         date = dateutil.parser.parse('1518-11-22').date(),
                         minutes = 49,
                         event_type = EventType.FALL_ASLEEP)

        actual = Event.from_string(target)
        assert expected == actual

    def test_parse_arrives(self):
        target = '[1518-11-22 00:49] Guard #1234 begins shift'
        expected = Event(guard_id = 1234,
                         date = dateutil.parser.parse('1518-11-22').date(),
                         minutes = 49,
                         event_type = EventType.BEGIN_SHIFT)

        actual = Event.from_string(target)
        assert expected == actual

    def test_parse_arrives_early(self):
        target = '[1518-11-22 23:49] Guard #1234 begins shift'
        expected = Event(guard_id = 1234,
                         date = dateutil.parser.parse('1518-11-22').date(),
                         minutes = -11,
                         event_type = EventType.BEGIN_SHIFT)

        actual = Event.from_string(target)
        assert expected == actual
