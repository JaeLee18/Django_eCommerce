from django.db import models
from member.models import Member, Member_cart
from apply.models import Apply
from django.utils import timezone
# 할인 정보
class Discount(models.Model):
	DISCOUNT_SET=(('1주년', '1000'), ('2주년', '20000'))
	off = models.CharField(max_length=5, choices = DISCOUNT_SET, null=True, blank=True)
	def __str__(self):
		return self.off 

# 택배비
class Shipping_fee(models.Model):
	FEES = ((3100, '우체국'), (5000, '새벽배송'))
	fee = models.CharField(max_length=10, choices = FEES, null=True)
	def __str__(self):
		return self.fee

# 전체 가격
class Price(models.Model):
	shipping_fee = models.ForeignKey(Shipping_fee, null=True)
	discount = models.ForeignKey(Discount, null=True)
	final_price = models.IntegerField(default = 0, blank=False, null=True)
	def __str__(self):
		return str(self.final_price)

# 주문 상태
class Order_status(models.Model):
	#order = models.ForeignKey('Order', null=True, blank=True)
	ORDER_STEPS = (('0', '주문접수'), ('1', '배송준비'), ('12', '단품 배송준비'), ('13', '단품 배송중'), ('14', '단품 배송완료'),
					('22', '프로그램 배송준비'), ('23', '프로그램 배송중'), ('24', '프로그램 배송준비'),
					('32', '박스 배송대기'), ('33', '박스 배송준비'), ('34', '박스 배송중'), ('35', '박스 배송완료'))
	status = models.CharField(max_length=1, choices = ORDER_STEPS, null=True)
	def __str__(self):
		return self.status

# 주문 결제 방법
class Order_payment(models.Model):
	order = models.ForeignKey('Order', null=True, blank=True)
	OPTIONS = (('카드','카드'), ('현금', '현금'))
	choice = models.CharField(max_length=10, choices=OPTIONS, null=True)
	def __str__(self):
		if self.choice is not None:
			return self.choice
# 택배회사
class Shipping_company(models.Model):
	COMPANIES = (('1', 'A'), ('2', 'B'))
	company = models.CharField(max_length=1, null=True, choices = COMPANIES)
	def __str__(self):
		return self.company

# 식단 기간
class Shipping_duration(models.Model):
	DURATIONS = (('1주', 7), ('2주', 14))
	duration = models.CharField(max_length=5, null=True, choices=DURATIONS)
	def __str__(self):
		return self.duration

# 식단 1주일에 몇번
class Shipping_iterate(models.Model):
	OPTIONS = (('1번', 1), ('2번' , 2))
	times = models.CharField(max_length=10, null=True, choices=OPTIONS)
	def __str__(self):
		return self.times

# 주문 정보
class Shipping_info(models.Model):
	#order = models.ForeignKey('Order', null=True)
	CHOCIES = (('0', '기본 배송지'), ('1', '주문자 정보와 동일'), ('2', '최근 배송지'), ('3', '새로운 배송	'))
	HOW_CHOICE = (('0','새벽배송(수도권 일부지역만 가능)'), ('1', '우체국배송'))
	DOORS = (('0', '비밀번호'), ('1', '주문자 전화'), ('2', '수령자 전화'), ('3', '경비실 배송'),
			('4', '경비실 호출'), ('5', '자유출입'))
	# 배송지 선택
	to_where = models.CharField(max_length=1, choices = CHOCIES, null=True, default='기본 배송지')
	# 받으시는 분
	whom = models.CharField(max_length=99, null=True, blank=True)
	# 주소
	delivery_address = models.CharField(null=True, max_length = 128)
	# 핸드폰
	cell = models.CharField(null=True, max_length=11,blank=True)
	# 전화번호
	phone = models.CharField(null=True, max_length=15, blank=True)
	# 배송방법
	how = models.CharField(max_length=1, choices=HOW_CHOICE, blank=True, null=True)
	# 공동현관 출입방법
	door = models.CharField(max_length=1, choices = DOORS, blank=True, null=True)
	# 공동현관 비밀번호
	door_pw = models.CharField(max_length=20, blank=True, null=True)
	# 현관 비밀번호 저장
	door_pw_save = models.BooleanField(blank=True,default=True)
	# 배송시 요청사항
	requests = models.TextField(blank=True, null=True)
	# 택배사
	company = models.ForeignKey(Shipping_company, null=True)
	# 몇주 짜리 프로그램?
	duration = models.ForeignKey(Shipping_duration, blank=True, null=True, default=7)
	# 주당 몇번 받을건지
	iteration = models.ForeignKey(Shipping_iterate, blank=True,null=True, default=2)
	def __str__(self):
		if self.whom is not None:
			return "Order to : " + self.whom
		else:
			return "error"

# 주문
class Order(models.Model):
	uni_id = models.CharField(null=True, max_length=16)
	member = models.ForeignKey(Member, null=True, blank=True)
	cart = models.ForeignKey(Member_cart, null=True)
	shipping = models.ForeignKey(Shipping_info, null=True,blank=True)
	price = models.ForeignKey(Price, null=True,blank=True)
	status = models.ForeignKey(Order_status, null=True, blank=True)
	# 주문한 순간
	order_date = models.DateTimeField(null=True,blank=True)
	comment = models.TextField(null=True, max_length=128, blank=True)
	# KCP 모듈 정보
	module_info = models.IntegerField(null=True, blank=False, default=0)
	# 배송된 횟수
	delivered = models.IntegerField(default=0, null=True)
	# 배송되어야 할 횟수
	toBdelivered = models.IntegerField(default=0, null=True)
	# 회원/비회원 유무
	isMember = models.BooleanField(default=False)
	# 시작하는 날
	start = models.DateField(null=True, blank=True)
	# 끝나는 날
	#end = models.DateField(null=True, blank=True)
	
	def __str__(self):
		return str(self.order_date)




