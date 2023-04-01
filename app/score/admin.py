from django.contrib import admin
from .models import ScoreBoardModel


# Register your models here.
class ScoreBoardAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "time")
    list_filter = ("user", "time")
    search_fields = ("user__username__startswith",)
    ordering = ("-score",)


admin.site.register(ScoreBoardModel, ScoreBoardAdmin)
