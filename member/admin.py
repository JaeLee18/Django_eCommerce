from django.contrib import admin
from .models import *
from account.models import Profile 
from tracking.models import OrderTracking

#admin.site.register(Customer, CustomerAdmin)
class InfoAdminInline(admin.TabularInline):
	model = Member_info
	extra = 0

class ServiceAdminInline(admin.TabularInline):
	model = Member_service
	extra = 0

class AddressAdminInline(admin.TabularInline):
	model = Member_address
	extra = 0

class CartAdminInline(admin.TabularInline):
	model = Member_cart
	extra = 0
	ordering = ('-date',)
	
class CalendarAdminInline(admin.TabularInline):
	model = Member_calendar
	extra = 0

class Tracking(admin.TabularInline):
	model = OrderTracking
	extra = 0
class MemberAdmin(admin.ModelAdmin):
	list_display=('member',)
	inlines = [AddressAdminInline, InfoAdminInline, ServiceAdminInline, CartAdminInline ,Tracking]

admin.site.register(Member, MemberAdmin)
#admin.site.register(Customer_info)
#admin.site.register(Customer_service)
admin.site.register(Member_address)
admin.site.register(Member_cart)
#admin.site.register(Customer_calendar)
