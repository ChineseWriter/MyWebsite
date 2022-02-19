# coding = UTF-8


from django.db import models
from django.utils.translation import gettext_lazy


class SupportWebsite(models.TextChoices):
    KuGou = "KG", gettext_lazy("酷狗音乐")
    WangYiYun = "WYY", gettext_lazy("网易云音乐")
    QQMusic = "QM", gettext_lazy("QQ音乐")
    BaiduPicture = "DP", gettext_lazy("百度图片")
    BingPicture = "BP", gettext_lazy("必应图片")


class Poster(models.Model):
    name = models.CharField(max_length=20, verbose_name="海报名称", null=True, blank=True)
    source_site = models.CharField(max_length=5, verbose_name="来源网站", choices=SupportWebsite.choices)
    self_source = models.URLField(verbose_name="海报来源")
    self_object = models.ImageField(verbose_name="海报文件", upload_to="posters/%Y/%m/%d/")
    description = models.TextField(verbose_name="海报描述", null=True, blank=True)


class Singer(models.Model):
    name = models.CharField(max_length=20, verbose_name="演唱者名称")
    source_site = models.CharField(max_length=5, verbose_name="来源网站", choices=SupportWebsite.choices)
    master_id = models.CharField(max_length=30, verbose_name="演唱者ID")
    description = models.TextField(verbose_name="演唱者简介")
    posters = models.ManyToManyField(Poster, verbose_name="演唱者海报")

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=30, verbose_name="歌曲名称")
    source_site = models.CharField(max_length=5, verbose_name="来源网站", choices=SupportWebsite.choices)
    self_source = models.URLField(verbose_name="歌曲来源")
    self_object = models.FileField(verbose_name="歌曲文件", upload_to="musics/%Y/%m/%d/")
    singers = models.ManyToManyField(Singer, verbose_name="歌曲演唱者")
    posters = models.ManyToManyField(Poster, verbose_name="歌曲海报")
    lyrics = models.TextField(verbose_name="歌曲歌词")
    album = models.CharField(max_length=20, verbose_name="歌曲专辑")
    mv = models.FileField(verbose_name="歌曲MV", upload_to="mv/%Y/%m/%d/", null=True, blank=True)
    mv_source = models.URLField(verbose_name="MV来源", null=True, blank=True)
    master_id = models.CharField(max_length=30, verbose_name="主ID")
    sub_id = models.CharField(max_length=30, verbose_name="副ID")

    def __str__(self):
        return self.name


