from collections import defaultdict
from typing import List, Tuple, Dict, Set
from validations import is_valid_days_list

# Threshold constants for easy configuration
MIN_DAYS: int = 2
MIN_INTERSECTIONS: int = 2


def update_event_intersections(day: List[Tuple[str, str]]) -> Dict[str, Set[str]]:
    event_intersections: Dict[str, Set[str]] = defaultdict(set)
    for intersection, event in day:
        event_intersections[event].add(intersection)
    return event_intersections


def update_event_days_count(event_intersections: Dict[str, Set[str]], event_days_count: Dict[str, int], critical_events: Set[str]):
    for event, intersections in event_intersections.items():
        if len(intersections) >= MIN_INTERSECTIONS:
            event_days_count[event] += 1
            if event_days_count[event] >= MIN_DAYS:
                critical_events.add(event)


def find_critical_events(days_list: List[List[Tuple[str, str]]]) -> List[str]:
    if not is_valid_days_list(days_list):
        return []

    event_days_count: Dict[str, int] = defaultdict(int)
    critical_events: Set[str] = set()

    for day in days_list:
        event_intersections = update_event_intersections(day)
        update_event_days_count(event_intersections, event_days_count, critical_events)

    return list(critical_events)