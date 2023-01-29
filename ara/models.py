# Copyright (c) 2022 The ARA Records Ansible authors
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from django.db import models
from django.utils import timezone

from model_utils.models import TimeFramedModel, TimeStampedModel
from model_utils.fields import StatusField, UUIDField


class DurationModel(TimeFramedModel, TimeStampedModel):
    """
    Abstract model for models with a concept of duration
    """

    class Meta:
        abstract = True

    duration = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Compute duration based on available timestamps
        if self.ended is not None:
            self.duration = self.ended - self.started
        return super().save(*args, **kwargs)


class Label(TimeStampedModel):
    """
    A label is a generic container meant to group or correlate different
    playbooks. It could be a single playbook run. It could be a "group" of
    playbooks.
    It could represent phases or dynamic logical grouping and tagging of
    playbook runs.
    You could have a label named "failures" and make it so failed playbooks
    are added to this report, for example.
    The main purpose of this is to make the labels customizable by the user.
    """

    class Meta:
        db_table = "labels"

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"<Label {self.name}: {self.id}>"


class Playbook(DurationModel):
    """
    An entry in the 'playbooks' table represents a single execution of the
    ansible or ansible-playbook commands. All the data for that execution
    is tied back to this one playbook.
    """

    # A playbook in ARA can be running (in progress), completed (succeeded) or failed.
    UNKNOWN = "unknown"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    STATUS = (
        (UNKNOWN, "unknown"),
        (EXPIRED, "expired"),
        (RUNNING, "running"),
        (COMPLETED, "completed"),
        (FAILED, "failed"),
    )

    name = models.CharField(max_length=255, null=True)

    ansible_version = models.CharField(max_length=255)
    client_version = models.CharField(max_length=255, null=True)
    python_version = models.CharField(max_length=255, null=True)
    server_version = models.CharField(max_length=255)

    status = StatusField()

    controller = models.CharField(max_length=255, null=True, default="localhost")
    arguments = models.BinaryField(max_length=(2**32) - 1)
    path = models.CharField(max_length=255)

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="playbooks",
    )
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return f"<Playbook {self.id}>"


class FileContent(TimeStampedModel):
    """
    Contents of a uniquely stored and compressed file.
    Running the same playbook twice will yield two playbook files but just
    one file contents.
    """

    sha1 = models.CharField(max_length=40, unique=True)
    contents = models.BinaryField(max_length=(2**32) - 1)

    def __str__(self):
        return f"<FileContent {self.id}: {self.sha1}>"


class File(TimeStampedModel):
    """
    Data about Ansible files (playbooks, tasks, role files, var files, etc).
    Multiple files can reference the same FileContent record.
    """

    path = models.CharField(max_length=255)

    content = models.ForeignKey(
        "FileContent",
        on_delete=models.CASCADE,
        related_name="files",
    )
    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="files",
    )

    def __str__(self):
        return f"<File {self.id}: {self.path}>"


class Record(TimeStampedModel):
    """
    A rudimentary key/value table to associate arbitrary data to a playbook.
    Used with the ara_record and ara_read Ansible modules.
    """

    value = models.BinaryField(max_length=(2**32) - 1)
    key = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    playbook = models.ForeignKey(
        Playbook,
        on_delete=models.CASCADE,
        related_name="records",
    )

    def __str__(self):
        return f"<Record {self.id}: {self.key}>"


class Play(DurationModel):
    """
    Data about Ansible plays.
    Hosts, tasks and results are childrens of an Ansible play.
    """

    # A play in ARA can be running (in progress) or completed (regardless of success or failure)
    UNKNOWN = "unknown"
    RUNNING = "running"
    COMPLETED = "completed"
    EXPIRED = "expired"
    STATUS = (
        (UNKNOWN, "unknown"),
        (RUNNING, "running"),
        (COMPLETED, "completed"),
        (EXPIRED, "expired"),
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    uuid = UUIDField()

    status = StatusField()

    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="plays",
    )

    def __str__(self):
        return f"<Play {self.id}: {self.name}>"


class Task(DurationModel):
    """Data about Ansible tasks."""

    # Possible statuses for a task
    # A failed task is expected to have at least one failed result
    UNKNOWN = "unknown"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    RUNNING = "running"

    STATUS = (
        (UNKNOWN, "unknown"),
        (COMPLETED, "completed"),
        (EXPIRED, "expired"),
        (FAILED, "failed"),
        (RUNNING, "running"),
    )

    action = models.TextField()
    handler = models.BooleanField()
    lineno = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    tags = models.BinaryField(max_length=(2**32) - 1)
    uuid = UUIDField()

    status = StatusField()

    file = models.ForeignKey("File", on_delete=models.CASCADE, related_name="tasks")
    play = models.ForeignKey("Play", on_delete=models.CASCADE, related_name="tasks")
    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    def __str__(self):
        return f"<Task {self.id}: {self.name}>"


class Host(TimeStampedModel):
    """
    Data about Ansible hosts.
    """

    name = models.CharField(max_length=255)
    facts = models.BinaryField(max_length=(2**32) - 1)

    changed = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    ok = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    unreachable = models.IntegerField(default=0)

    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="hosts",
    )

    def __str__(self):
        return f"<Host {self.id}: {self.name}>"


class LatestHost(TimeStampedModel):
    """
    Latest record of each host based on name, referring to `Host` object id related.

    We can not inherit from TimeStampedModel because we want to use `name` as primary key.
    """

    name = models.CharField(max_length=255, primary_key=True)

    host = models.ForeignKey(Host, on_delete=models.CASCADE)

    def __str__(self):
        return f"<LatestHost {self.id}: {self.name}>"


class Result(DurationModel):
    """
    Data about Ansible results.
    A task can have many results if the task is run on multiple hosts.
    """

    # Ansible statuses
    OK = "ok"
    FAILED = "failed"
    SKIPPED = "skipped"
    UNREACHABLE = "unreachable"
    # ARA specific status, it's the default when not specified
    UNKNOWN = "unknown"

    # fmt:off
    STATUS = (
        (OK, "ok"),
        (FAILED, "failed"),
        (SKIPPED, "skipped"),
        (UNREACHABLE, "unreachable"),
        (UNKNOWN, "unknown"),
    )
    # fmt:on

    status = StatusField()

    changed = models.BooleanField(default=False)
    ignore_errors = models.BooleanField(default=False)

    content = models.ForeignKey(
        "Content",
        on_delete=models.CASCADE,
        related_name="content_results",
    )
    host = models.ForeignKey(
        "Host",
        on_delete=models.CASCADE,
        related_name="host_results",
    )
    delegated_to = models.ManyToManyField(
        Host,
        related_name="delegated_results",
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="task_results",
    )
    play = models.ForeignKey(
        "Play",
        on_delete=models.CASCADE,
        related_name="play_results",
    )
    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="palybook_results",
    )

    def __str__(self):
        return f"<Result {self.id}: {self.status}>"


class Content(models.Model):
    """
    Content is a generic table to store data that is not directly related to
    Ansible but that we want to keep track of.
    """

    # Content types
    LOG = "log"
    STDOUT = "stdout"
    STDERR = "stderr"
    TRACEBACK = "traceback"

    TYPE = (
        (LOG, "log"),
        (STDOUT, "stdout"),
        (STDERR, "stderr"),
        (TRACEBACK, "traceback"),
    )

    type = StatusField(choices_name="TYPE")
    content = models.BinaryField(max_length=(2**32) - 1)

    result = models.ForeignKey(
        "Result",
        on_delete=models.CASCADE,
        related_name="result_content",
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="task_content",
    )
    play = models.ForeignKey(
        "Play",
        on_delete=models.CASCADE,
        related_name="play_content",
    )
    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="playbook_content",
    )

    def __str__(self):
        return f"<Content {self.id}: {self.type}>"
