from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from apply.models import Coupon
from account.models import Profile
from date.models import Availble_date, Not_availble_date
from product.models import Product, Program
from django.contrib.postgres.fields import ArrayField

# 고객
class Member(models.Model):
	TYPE = (('0', '비회원'), ('1', '회원'), ('2', 'NAVER'), ('3', 'KAKAO'))
	member = models.ForeignKey(Profile, null=True)
	isRegistered = models.CharField(max_length=1, choices=TYPE, null=True,default='0')
	indicator = models.CharField(max_length=16,null=True,blank=True)
	def __str__(self):
		if self.isRegistered == '1':
			return "[name]:"+self.member.user.first_name
		else:
			return "비회원"
# CS 관리 DB
class Member_service(models.Model):
	member = models.ForeignKey(Member, null=True)
	# 고객에 대한 주의사항, 또는.... 아무거나
	comments = models.TextField(null=True, blank=True)
	def __str__(self):
		return "[name]:"+self.member.member.user.first_name

# 고객 정보
class Member_info(models.Model):
	member = models.ForeignKey(Member, null=True)
	coupon = models.ForeignKey(Coupon, null=True)
	customer_etc = models.TextField(null=True, blank=True)
	def __str__(self):
		return "[name]:"+self.member.member.user.first_name


# 고객 주소
class Member_address(models.Model):
	member = models.ForeignKey(Member, null=True)
	descr = models.CharField(max_length=128, null=True)
	# 주소 1
	address1 = models.CharField(max_length=128, null=True, blank=True)
	# 주소 2
	address2 = models.CharField(max_length=128, null=True, blank=True)
	# 주소 3
	address3 = models.CharField(max_length=128, null=True, blank=True)
	def __str__(self):
		return "[name]:"+self.member.member.user.first_name +" 의 " + self.descr

# 고객 장바구니
class Member_cart(models.Model):
	member = models.ForeignKey(Member, null=True, blank=True)
	product = models.ManyToManyField(Product,blank=True)
	program = models.ManyToManyField(Program,  blank=True)
	# 최종 금액
	final_price = models.IntegerField(default = 0, null=True, blank=False)
	# 카트가 생성된 시간
	date = models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
		return " [price]:" + str(self.final_price)
		#return "[name]:"+self.member.member.user.first_name + " [price]:" + str(self.final_price)
		#return "Program: " + '-'.join([str(Program.name) for Program in self.program.all()])

# 고객 달력
class Member_calendar(models.Model):
	STAT = (('1', '사유들'),)
	member = models.ForeignKey(Member, null=True)
	# 원래 날짜들
	original = models.ManyToManyField(Availble_date, blank=True)
	# 변경된 날짜들
	modified = models.ManyToManyField(Not_availble_date,  blank=True)
	# 현 상태
	status = models.CharField(max_length=100, null=True, blank=True, choices = STAT)
	# 고객에대한?s
	comment = models.TextField(null=True, blank=True)
	