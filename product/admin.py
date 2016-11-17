from django.contrib import admin
from .models import *


class ScheduleAdminInline(admin.TabularInline):
    model = Schedule
    extra = 0

class ProductAdmin(admin.ModelAdmin):
	list_filter = ('percent_cal',)
	search_fields = ('name', 'code')
	list_display = ('id', 'code', 'name','short_description',)

	inlines=[ScheduleAdminInline]

class ProgramOptionAdminInline(admin.TabularInline):
	model = Program_options
	extra = 0

class Programduration(admin.TabularInline):
	model = Program_duration
	extra = 0
class ProgramAdmin(admin.ModelAdmin):
	inlines = [ProgramOptionAdminInline, Programduration]

admin.site.register(Product, ProductAdmin)
admin.site.register(Product_picture)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Special)

admin.site.register(Option)
#admin.site.register(Program_options)

admin.site.register(Schedule)
admin.site.register(Program_duration)