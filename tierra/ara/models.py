from django.contrib.auth import get_user_model
from django.db import models
from model_utils.fields import StatusField, UUIDField
from model_utils.models import TimeFramedModel, TimeStampedModel

from .conf import (
    CONTENT_STATUS,
    DEFAULT_CONTROLLER,
    PLAY_STATUS,
    PLAYBOOK_STATUS,
    RESULT_STATUS,
    TASK_STATUS,
)

User = get_user_model()


class DurationModel(TimeFramedModel, TimeStampedModel):
    """
    Abstract model for models with a concept of duration
    """

    duration = models.DurationField(blank=True, null=True)

    class Meta:
        abstract = True


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

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"<Label {self.name}: {self.id}>"


class Playbook(DurationModel):
    """
    An entry in the 'playbooks' table represents a single execution of the
    ansible or ansible-playbook commands. All the data for that execution
    is tied back to this one playbook.
    """

    STATUS = PLAYBOOK_STATUS

    ansible_version = models.CharField(max_length=255)
    arguments = models.BinaryField(max_length=(2**32) - 1)
    client_version = models.CharField(max_length=255, null=True)
    controller = models.CharField(
        default=DEFAULT_CONTROLLER,
        max_length=255,
        null=True,
    )
    name = models.CharField(max_length=255, null=True)
    path = models.CharField(max_length=255)
    python_version = models.CharField(max_length=255, null=True)
    server_version = models.CharField(max_length=255)
    status = StatusField()

    labels = models.ManyToManyField("ara.Label")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="playbooks",
    )

    def __str__(self):
        return f"<Playbook {self.id}>"


class FileContent(TimeStampedModel):
    """
    Contents of a uniquely stored and compressed file.
    Running the same playbook twice will yield two playbook files but just
    one file contents.
    """

    contents = models.BinaryField(max_length=(2**32) - 1)
    sha1 = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"<FileContent {self.id}: {self.sha1}>"


class File(TimeStampedModel):
    """
    Data about Ansible files (playbooks, tasks, role files, var files, etc).
    Multiple files can reference the same FileContent record.
    """

    path = models.CharField(max_length=255)

    content = models.ForeignKey(
        "ara.FileContent",
        on_delete=models.CASCADE,
        related_name="files",
    )
    playbook = models.ForeignKey(
        "ara.Playbook",
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

    key = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    value = models.BinaryField(max_length=(2**32) - 1)

    playbook = models.ForeignKey(
        "ara.Playbook",
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

    STATUS = PLAY_STATUS

    name = models.CharField(max_length=255, blank=True, null=True)
    status = StatusField()
    uuid = UUIDField()

    playbook = models.ForeignKey(
        "Playbook",
        on_delete=models.CASCADE,
        related_name="plays",
    )

    def __str__(self):
        return f"<Play {self.id}: {self.name}>"


class Task(DurationModel):
    """Data about Ansible tasks."""

    STATUS = TASK_STATUS

    action = models.TextField()
    handler = models.BooleanField()
    lineno = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    status = StatusField()
    tags = models.BinaryField(max_length=(2**32) - 1)
    uuid = UUIDField()

    file = models.ForeignKey(
        "ara.File",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    play = models.ForeignKey(
        "ara.Play",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    playbook = models.ForeignKey(
        "ara.Playbook",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    def __str__(self):
        return f"<Task {self.id}: {self.name}>"


class Host(TimeStampedModel):
    """
    Data about Ansible hosts.
    """

    changed = models.IntegerField(default=0)
    facts = models.BinaryField(max_length=(2**32) - 1)
    failed = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
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

    host = models.ForeignKey(
        Host, on_delete=models.CASCADE, related_name="latest_hosts"
    )

    def __str__(self):
        return f"<LatestHost {self.id}: {self.name}>"


class Result(DurationModel):
    """
    Data about Ansible results.
    A task can have many results if the task is run on multiple hosts.
    """

    STATUS = RESULT_STATUS

    changed = models.BooleanField(default=False)
    ignore_errors = models.BooleanField(default=False)
    status = StatusField()

    delegated_to = models.ManyToManyField(
        Host,
        related_name="delegated_results",
    )
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
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="task_results",
    )

    def __str__(self):
        return f"<Result {self.id}: {self.status}>"


class Content(models.Model):
    """
    Content is a generic table to store data that is not directly related to
    Ansible but that we want to keep track of.
    """

    SATATUS = CONTENT_STATUS

    type = StatusField(choices_name="TYPE")
    content = models.BinaryField(max_length=(2**32) - 1)

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

    def __str__(self):
        return f"<Content {self.id}: {self.type}>"
