import pytest
from src.models import parse_events, only_level, count

def test_parse_event_valid_and_malformed():
    """Verifies structured parsing and skipping of lines without colons."""
    logs = ["INFO:system ready", "INVALID_LINE", "ERROR:failed"]
    parsed = list(parse_events(logs))

    assert len(parsed) == 2
    assert parsed[0] == ("INFO", "system ready")
    assert parsed[1] == ("ERROR", "failed")


def test_only_level_filtering():
    """Verifies that only the requested log level is yielded."""
    events = [("INFO", "a"), ("ERROR", "b"), ("INFO", "c")]
    filtered = list(only_level(iter(events), "INFO"))

    assert len(filtered) == 2
    assert all(level == "INFO" for level, msg in filtered)
    assert filtered[1][1] == "c"

def test_count_consumes_iterator():
    """Verifies that count correctly totals the items in an iterator."""
    events = [("DEBUG", "1"), ("DEBUG", "2"), ("DEBUG", "3")]
    # Wrap in iter() to simulate a generator
    assert count(iter(events)) == 3

def test_empty_pipline():
    """Verifies that the pipline handle empty input without errors."""
    parsed = parse_events([])
    filtered = only_level(parsed, "ERROR")
    assert count(filtered) == 0

def test_lazy_behavior_logic():
    """If we pass a list with an object that 
       raises an error on access, parse_events shouldn't hit it 
       until we actually iterate."""
    def infinite_logs():
        yield "INFO:first"
        yield "ERROR:second"
        raise RuntimeError("stop here")

    pipline = only_level(parse_events(infinite_logs()), "INFO")
    # We can get the first item without triggering the RuntimeError
    # that happens later in the generator.
    assert next(pipline) == ("INFO", "first")