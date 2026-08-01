"""
HomeLab OS — Remote Events Definition
"""

class RemoteEvents:
    LOGIN = "remote.login"
    LOGOUT = "remote.logout"
    COMMAND_EXECUTED = "remote.command.executed"
    COMMAND_FAILED = "remote.command.failed"
    SHUTDOWN = "remote.shutdown"
    RESTART = "remote.restart"
    FILE_DOWNLOAD = "remote.file.download"
    FILE_UPLOAD = "remote.file.upload"
