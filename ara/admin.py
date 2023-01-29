# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Label, Playbook, FileContent, File, Record, Play, Task, Host, LatestHost, Result, Content


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'name')
    list_filter = ('created', 'modified')
    search_fields = ('name',)


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'start',
        'end',
        'duration',
        'name',
        'ansible_version',
        'client_version',
        'python_version',
        'server_version',
        'status',
        'controller',
        'arguments',
        'path',
        'user',
    )
    list_filter = ('created', 'modified', 'start', 'end', 'user')
    raw_id_fields = ('labels',)
    search_fields = ('name',)


@admin.register(FileContent)
class FileContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'sha1', 'contents')
    list_filter = ('created', 'modified')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'path',
        'content',
        'playbook',
    )
    list_filter = ('created', 'modified', 'content', 'playbook')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'value',
        'key',
        'type',
        'playbook',
    )
    list_filter = ('created', 'modified', 'playbook')


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'modified',
        'start',
        'end',
        'duration',
        'name',
        'uuid',
        'status',
        'playbook',
    )
    list_filter = ('created', 'modified', 'start', 'end', 'playbook')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'modified',
        'start',
        'end',
        'duration',
        'action',
        'handler',
        'lineno',
        'name',
        'tags',
        'uuid',
        'status',
        'file',
        'play',
        'playbook',
    )
    list_filter = (
        'created',
        'modified',
        'start',
        'end',
        'handler',
        'file',
        'play',
        'playbook',
    )
    search_fields = ('name',)


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'name',
        'facts',
        'changed',
        'failed',
        'ok',
        'skipped',
        'unreachable',
        'playbook',
    )
    list_filter = ('created', 'modified', 'playbook')
    search_fields = ('name',)


@admin.register(LatestHost)
class LatestHostAdmin(admin.ModelAdmin):
    list_display = ('created', 'modified', 'name', 'host')
    list_filter = ('created', 'modified', 'host')
    search_fields = ('name',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'start',
        'end',
        'duration',
        'status',
        'changed',
        'ignore_errors',
        'content',
        'host',
        'task',
        'play',
        'playbook',
    )
    list_filter = (
        'created',
        'modified',
        'start',
        'end',
        'changed',
        'ignore_errors',
        'content',
        'host',
        'task',
        'play',
        'playbook',
    )
    raw_id_fields = ('delegated_to',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'content',
        'result',
        'task',
        'play',
        'playbook',
    )
    list_filter = ('result', 'task', 'play', 'playbook')
