# coding = UTF-8

from django.contrib import admin

from .models import ItemCategory, InventoryItems, Procurement, InventoryOperation


class InventoryItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("基本信息", {"fields": ["name", "category"]}),
        ("其它信息", {"fields": ["model", "unit", "brand"]})
    ]
    list_display = ["name", "model", "brand", "show_category"]
    list_filter = ["name"]


class ProcurementAdmin(admin.ModelAdmin):
    fieldsets = [
        ("基本信息", {"fields": ["goods", "procurement_time"]}),
        ("财务信息", {"fields": ["quantity", "unit_price"]})
    ]
    list_display = ["goods", "procurement_time", "show_total_price"]
    list_filter = ["goods", "procurement_time"]


class InventoryOperationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("基本信息", {"fields": ["operation", "operation_time"]}),
        ("物品信息", {"fields": ["goods", "quantity"]})
    ]
    list_display = ["operation", "operation_time", "goods", "quantity"]
    list_filter = ["operation", "operation_time", "goods"]


admin.site.register(ItemCategory)
admin.site.register(InventoryItems, InventoryItemsAdmin)
admin.site.register(Procurement, ProcurementAdmin)
admin.site.register(InventoryOperation, InventoryOperationAdmin)
