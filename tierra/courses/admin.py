from django.contrib import admin

from .models import Content, Course, File, Image, Module, Subject, Text, Video

# use memcache admin index site
# admin.site.index_template = "memcache_status/admin_index.html"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    search_fields = ("slug",)
    prepopulated_fields = {"slug": ("title",)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "created"]
    list_filter = ("owner", "subject", "created")
    raw_id_fields = ("students",)
    search_fields = ("slug", "title", "overview")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "title", "description", "order")
    list_filter = ("course",)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "module", "content_type", "object_id", "order")
    list_filter = ("module", "content_type")


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created", "updated", "content")
    list_filter = ("owner", "created", "updated")


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created", "updated", "file")
    list_filter = ("owner", "created", "updated")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created", "updated", "file")
    list_filter = ("owner", "created", "updated")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created", "updated", "url")
    list_filter = ("owner", "created", "updated")
