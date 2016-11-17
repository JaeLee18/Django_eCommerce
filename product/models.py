from django.db import models

# 식단, 프로그램들
class Program(models.Model):
	name = models.CharField(max_length =125, null=True)
	side = models.ManyToManyField('Option', null=True, blank=True)
	price = models.IntegerField(null=True,blank=False, default = 0)
	side = models.BooleanField(default=False)
	def __str__(self):
		return self.name

# 단품
class Product(models.Model):
	DAYS = (('0', '월'), ('1', '화'), ('2', '수'), ('3', '목'), ('4', '금'), ('5', '토'), ('6', '일'))
	program = models.ForeignKey(Program)
	code=models.CharField(blank=True, max_length=6)
	name=models.CharField(blank=True, max_length=255)
	# 닥키_첫번쨰줄
	firstRow = models.CharField(blank=True, max_length=12)
	# 닥키_두번쨰줄
	secondRow = models.CharField(blank=True, max_length=12)
	# 닥키_칼로리
	nuturition_cal=models.FloatField(blank=True,null=True,default=0)
	# 닥키_단백질
	nuturition_protein=models.FloatField(null=True,default=0,blank=True)
	# 닥키_지방
	nuturition_fat=models.FloatField(null=True,default=0,blank=True)
	# 닥키_탄수화물
	nuturition_car=models.FloatField(null=True,default=0,blank=True)
	# 닥키_당류
	nuturition_tsg=models.FloatField(null=True,default=0,blank=True)
	# 닥키_나트륨
	nuturition_sodium=models.FloatField(null=True,default=0,blank=True)
	# 닥키_콜레스트롤
	nuturition_cole=models.FloatField(null=True,default=0,blank=True)
	# 닥키_포화지방
	nuturition_sfa=models.FloatField(null=True,default=0,blank=True)
	# 닥키_트랜스지방
	nuturition_tfa=models.FloatField(null=True,default=0,blank=True)
	# 닥키_전체 식이섬유
	nuturition_tdf=models.FloatField(null=True,default=0,blank=True)
	# 닥키_단일불포화지방
	nuturition_mufa=models.FloatField(null=True,default=0,blank=True)
	# 닥키_다가불포화지방
	nuturition_fapu=models.FloatField(null=True,default=0,blank=True)

	# 긴 설명
	long_description = models.TextField(null=True,max_length=300,default=0,blank=True)
	# 짧은 설명
	short_description = models.CharField(max_length=50,null=True,default=0,blank=True)
	# 짧은 설명2
	short_description2 = models.CharField(max_length=50,null=True,default=0,blank=True)
	# 칼로리_퍼센트
	percent_cal = models.CharField(max_length=10,null=True,default=0,blank=True)
	# 당질 퍼센트
	percent_sugar = models.CharField(max_length=10,null=True,default=0,blank=True)
	# 포화지방 퍼센트
	percent_fat = models.CharField(max_length=10,null=True,default=0,blank=True)
	# 나트륨 퍼센트
	percent_sodium = models.CharField(max_length=10,null=True,default=0,blank=True)
	# 식이섬유 퍼센트
	percent_df = models.CharField(max_length=10,null=True,default=0,blank=True)
	# 불포화지방 퍼센트
	percent_uf = models.CharField(max_length=10,null=True,default=0,blank=True)
	# 상세보기 어떤 사진 나와야하나? ex) 75 = 75% 이하 ( 25,50,75)
	picture_index =models.IntegerField(null=True,blank=True)
	# 당질
	nuturition_glu =models.IntegerField(null=True,default=0,blank=True)
	# 불포화지방
	nuturition_uf = models.FloatField(null=True,default=0,blank=True)
	# 단품 금액
	price = models.IntegerField(null=True, blank=True)
	# 총 생산량
	count = models.IntegerField(null=True,blank=True)
	# 생산 되어야할 양
	toBproduced = models.IntegerField(null=True,blank=True, default = 0)
	# 생산 된 양
	amount = models.IntegerField(null=True,blank=True, default = 0)
	# 한계량
	limit = models.IntegerField(null=True,blank=True, default = 0)
	# 매진 유무
	sold_out = models.BooleanField(default=False)
	# 가능한 요일들
	days = models.CharField(max_length=1, choices=DAYS, null=True, blank= True)
	def __str__(self):
		return self.name
# 단품 사진
class Product_picture(models.Model):
	product = models.ForeignKey(Product, null =True)
	# 웹용 사진
	picture_web = models.CharField(max_length=255,blank=True, null=True)
	# 모바일 사진
	picture_mobile = models.CharField(max_length=255,blank=True, null=True)

# 특별 할인?
class Special(models.Model):
	name = models.CharField(max_length=156, null=True, blank=False)
	product = models.ForeignKey(Product)
	price = models.IntegerField(null=True, blank=True)
	date = models.DateField(blank=True, null=True)

# 옵션
class Option(models.Model):
	# 프로그램을 옵션으로
	itself = models.ForeignKey(Program, null=True, blank=True)
	# 옵션 설명
	descr = models.CharField(max_length=125, null=True)
	def __str__(self):
		return str(self.descr)
	

# 프로그램 옵션
class Program_options(models.Model):
	choice = models.ForeignKey(Option, null=True)
	its_program = models.ForeignKey(Program, null=True, blank=True)
	def __str__(self):
		if self.choice is not None:
			return self.choice.descr
		if self.its_program is not None:
			return self.its_program.name
			
class Schedule(models.Model):
	OPTION = (('1끼','오전'), ('2끼', '중석식'))
	product= models.ForeignKey(Product)
	# 식단 날짜
	date = models.DateField(null=True, blank=True)
	isActive = models.BooleanField(default=True)
	def __str__(self):
		return str(self.date)

class Program_duration(models.Model):
	program = models.ForeignKey(Program, null=True)
	duration = models.CharField(max_length=128, default="2주", null=True)
	def __str__(self):
		return self.duration








