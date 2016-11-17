from django.contrib import admin
from .models import *


class InfoAdminInline(admin.StackedInline):
	model = Shipping_info
	extra = 0

class PriceAdminInline(admin.TabularInline):
	model = Price
	extra = 0

class PaymentAdminInline(admin.TabularInline):
	model = Order_payment
	extra = 0

class StatusAdminInline(admin.TabularInline):
	model = Order_status
	extra = 0

class OrderAdmin(admin.ModelAdmin):
	inlines = [InfoAdminInline, PriceAdminInline, PaymentAdminInline,StatusAdminInline]

admin.site.register(Discount)
admin.site.register(Shipping_fee)
admin.site.register(Price)
#admin.site.register(Order_status)
#admin.site.register(Order_payment)
#admin.site.register(Program_date)
admin.site.register(Shipping_company)
admin.site.register(Shipping_duration)
admin.site.register(Shipping_iterate)
admin.site.register(Shipping_info)
admin.site.register(Order)
