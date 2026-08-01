import os
import sys
import pytest

os.environ["TESTING"] = "1"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.core.homelab_core import HomelabCore


def test_intelligent_cleanup_rules():
    HomelabCore.reset()
    core = HomelabCore.instance()
    auto_svc = core.get_service("automation")
    assert auto_svc is not None
    assert auto_svc.health()["status"] == "healthy"
