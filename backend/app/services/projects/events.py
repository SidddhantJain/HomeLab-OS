"""
HomeLab OS — Project & Snapshot Event Definitions
"""

class ProjectEvents:
    CREATED = "projects.created"
    ACTIVE = "projects.active"
    ARCHIVED = "projects.archived"
    DELETED = "projects.deleted"


class SnapshotEvents:
    CREATED = "snapshot.created"
    DELETED = "snapshot.deleted"
    RESTORED = "snapshot.restored"
