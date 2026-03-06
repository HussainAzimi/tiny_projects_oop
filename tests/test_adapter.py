import pytest

from src.models import VendorLogger, VendorLoggerAdapter, process_event

def test_adapter_translation_logic(capsys):
    """Verifies that string levels are correctly mapped to vendor integers."""
    vendor = VendorLogger()
    adapter = VendorLoggerAdapter(vendor)
    
    # Test a specific mapping: ERROR should become 40
    adapter.log("ERROR", "System failure")
    
    captured = capsys.readouterr()
    assert "40, System failure" in captured.out

def test_adapter_invalid_level_raises_error():
    """Verifies that unknown log levels raise a ValueError."""
    adapter = VendorLoggerAdapter(VendorLogger())
    
    with pytest.raises(ValueError, match="Unknown log level"):
        adapter.log("FATAL", "Not in the map")

def test_process_event_integration(capsys):
    """Verifies that the business logic correctly interacts with the Adapter."""
    vendor = VendorLogger()
    adapter = VendorLoggerAdapter(vendor)
    
    # process_event is hardcoded to use "INFO" (which is 20)
    process_event(adapter, "DataBackup")
    
    captured = capsys.readouterr()
    assert "20, processed: DataBackup" in captured.out

def test_adapter_is_case_insensitive(capsys):
    """Verifies robustness by checking if lowercase levels still map correctly."""
    vendor = VendorLogger()
    adapter = VendorLoggerAdapter(vendor)
    
    # Should handle "debug" same as "DEBUG" (10)
    adapter.log("debug", "lowercase test")
    
    captured = capsys.readouterr()
    assert "10, lowercase test" in captured.out