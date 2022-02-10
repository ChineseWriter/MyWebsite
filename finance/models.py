# coding = UTF-8

from django.db import models
from django.contrib import admin


class ItemCategory(models.Model):
    category = models.CharField(max_length=10, verbose_name="仓库物品的类别")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "物品类别"


class InventoryItems(models.Model):
    name = models.CharField(max_length=50, verbose_name="仓库物品的名称")
    category = models.ManyToManyField(ItemCategory, verbose_name="仓库物品的类别")
    model = models.CharField(max_length=100, verbose_name="仓库物品的型号")
    brand = models.CharField(max_length=50, verbose_name="仓库物品的品牌")
    unit = models.CharField(max_length=5, verbose_name="仓库物品的单位")

    @admin.display(boolean=True, description="仓库物品的类别")
    def show_category(self, obj):
        return ",".join([category.category for category in obj.category.all()])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "仓库物品信息"


class Procurement(models.Model):
    procurement_time = models.DateTimeField(verbose_name="采购时间")
    goods = models.ForeignKey(InventoryItems, models.PROTECT, verbose_name="仓库物品")
    quantity = models.IntegerField(verbose_name="采购数量")
    unit_price = models.FloatField(verbose_name="物品单价")

    @admin.display(boolean=True, description="物品总价")
    def show_total_price(self, obj):
        return obj.quantity + obj.unit_price

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = "采购记录"


class InventoryOperation(models.Model):
    PUT_IN_STORAGE = "PIS"
    CHECK_OUT_STORAGE = "COS"
    OPERATION_CHOICES = [
        (PUT_IN_STORAGE, "入库"),
        (CHECK_OUT_STORAGE, "出库")
    ]

    operation_time = models.DateTimeField(verbose_name="操作时间")
    operation = models.CharField(max_length=5, choices=OPERATION_CHOICES, verbose_name="操作")
    goods = models.ForeignKey(InventoryItems, models.PROTECT, verbose_name="仓库物品")
    quantity = models.IntegerField(verbose_name="操作数量")

    def __str__(self):
        return self.operation

    class Meta:
        verbose_name = "仓库操作记录"

