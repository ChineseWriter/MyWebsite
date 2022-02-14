# coding = UTF-8

from django.contrib import admin

from .models import Poster, Singer, Music


class PosterAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    fieldsets = [
        ("基本信息", {"fields": ["name", "source_site"]}),
        ("其余信息", {"fields": ["self_source", "description"]}),
        ("文件", {"fields": ["self_object"]})
    ]
    list_display = ["name", "source_site"]
    list_filter = ["name"]
    search_fields = ["name"]


class SingerAdmin(admin.ModelAdmin):
    list_per_page = 50
    actions_on_top = True
    actions_on_bottom = True
    fieldsets = [
        ("基本信息", {"fields": ["name", "source_site"]}),
        ("其余信息", {"fields": ["description", "posters"]}),
        ("编号信息", {"fields": ["master_id"]})
    ]
    list_display = ["name", "source_site"]
    list_filter = ["name", "source_site"]
    search_fields = ["name", "source_site"]


class MusicAdmin(admin.ModelAdmin):
    list_per_page = 100
    actions_on_top = True
    actions_on_bottom = True
    fieldsets = [
        ("基本信息", {"fields": ["name", "album", "source_site"]}),
        ("其余信息", {"fields": ["lyrics", "posters", "singers"]}),
        ("文件信息", {"fields": ["self_source", "self_object"]}),
        ("MV信息", {"fields": ["mv_source", "mv"]}),
        ("ID信息", {"fields": ["master_id", "sub_id"]}),
    ]
    list_display = ["name", "album", "source_site", "music_singers"]
    list_filter = ["source_site"]
    search_fields = ["name", "album", "source_site"]

    @admin.display(description="歌曲演唱者")
    def music_singers(self, obj):
        return [one_singer.name for one_singer in obj.singers.all()]


admin.site.register(Poster, PosterAdmin)
admin.site.register(Singer, SingerAdmin)
admin.site.register(Music, MusicAdmin)
