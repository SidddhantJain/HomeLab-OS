import os
import sys
import pytest

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.services.storage.intelligence import StorageIntelligenceEngine


def test_storage_intelligence_analytics():
    engine = StorageIntelligenceEngine()
    dupes = engine.analyze_duplicates()
    assert isinstance(dupes, list)

    large = engine.analyze_large_files()
    assert isinstance(large, list)

    fc = engine.forecast_capacity()
    assert "current_usage_gb" in fc
    assert fc["estimated_full_days"] > 0
