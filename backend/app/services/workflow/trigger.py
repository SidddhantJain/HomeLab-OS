"""
HomeLab OS — Workflow Triggers Definition
"""

import enum


class TriggerType(str, enum.Enum):
    TIME = "time"
    EVENT = "event"
    THRESHOLD = "threshold"
    MANUAL = "manual"
