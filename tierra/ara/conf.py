# A playbook in ARA can be running (in progress), completed (succeeded) or failed.
COMPLETED = "completed"
EXPIRED = "expired"
FAILED = "failed"
RUNNING = "running"
UNKNOWN = "unknown"

# Ansible statuses

OK = "ok"
SKIPPED = "skipped"
UNREACHABLE = "unreachable"

# Content types
LOG = "log"
STDOUT = "stdout"
STDERR = "stderr"
TRACEBACK = "traceback"

PLAYBOOK_STATUS = (
    (COMPLETED, "completed"),
    (EXPIRED, "expired"),
    (FAILED, "failed"),
    (RUNNING, "running"),
    (UNKNOWN, "unknown"),
)

# A play in ARA can be running (in progress) or completed (regardless of success or failure)
PLAY_STATUS = (
    (COMPLETED, "completed"),
    (EXPIRED, "expired"),
    (RUNNING, "running"),
    (UNKNOWN, "unknown"),
)

TASK_STATUS = PLAYBOOK_STATUS


RESULT_STATUS = (
    (OK, "ok"),
    (FAILED, "failed"),
    (SKIPPED, "skipped"),
    (UNREACHABLE, "unreachable"),
    (UNKNOWN, "unknown"),
)

CONTENT_STATUS = (
    (LOG, "log"),
    (STDOUT, "stdout"),
    (STDERR, "stderr"),
    (TRACEBACK, "traceback"),
)

DEFAULT_CONTROLLER = "localhost"

__all__ = [
    "CONTENT_STATUS",
    "DEFAULT_CONTROLLER",
    "PLAY_STATUS",
    "PLAYBOOK_STATUS",
    "RESULT_STATUS",
    "TASK_STATUS",
]
