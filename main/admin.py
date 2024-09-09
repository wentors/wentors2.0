from django.contrib import admin
from .models import SubscriptionPlan, CohortSchedule

# Register your models here.\

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description",)
    list_filter = ("name", "price", )

@admin.register(CohortSchedule)
class CohortSchedule(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "description")
    list_filter = ("start_date",)
