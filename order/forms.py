from django import forms
from .models import *
from django.forms.extras.widgets import SelectDateWidget

class shippingForm(forms.ModelForm):
	class Meta:
		model = Shipping_info
		fields = "__all__"
		exclude = ('company',)

class checkOrderGuest(forms.Form):
	# 주문번호 
	uuid = forms.CharField()

class applyForm(forms.Form):
	twoweeks = forms.BooleanField(required=False)
	fourweeks = forms.BooleanField(required=False)
	oneMeal = forms.BooleanField(required=False)
	twoMeals = forms.BooleanField(required=False)
	side = forms.BooleanField(required=False,initial=False)
	ppl = forms.IntegerField(required=False,initial=1)
	start = forms.DateField()


class durationForm(forms.Form):
	# 이날부터 안먹음
	from_date = forms.DateField()
	# 이날부터 다시 먹
	new_start = forms.DateField()