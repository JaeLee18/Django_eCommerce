from django.shortcuts import render
from .models import *
from .forms import shippingForm, checkOrderGuest, applyForm, durationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from account.forms import LoginForm
from django.contrib.auth.models import User
from account.models import Profile
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from product.models import Program, Program_duration, Product, Schedule
from django.shortcuts import render_to_response, redirect
from tracking.models import OrderTracking
import datetime
from member.models import *


"""
실제로 주문을 하는 페이지.
이 페이지에서 2주,4주, 반찬유무를 고르고
마지막에 시작일을 고름.
"""
def OrderRequest(request):
    if request.method == 'POST':
        orderForm = applyForm(request.POST)
        if orderForm.is_valid():  
            
            request.session['date'] = orderForm['start'].value()
            # Type Casting from String to Date
            try:
                d = datetime.datetime.strptime(orderForm['start'].value(), '%Y-%m-%d').date()
            except:
                return HttpResponse("Check your start date")
            product = None
            program = None
            # Registed Customer
            if request.user.is_authenticated():
                profile = Profile.objects.get(user=request.user)
                member = Member.objects.get(member=profile)
                # Save member status to '회원'
                member.isRegistered = '1'
                member.save()

                # Get a cart object
                cart = Member_cart.objects.create(member=member)
                # 2주 식단
                if orderForm['twoweeks'].value() == True:
                    request.session['week']=2
                    if orderForm['oneMeal'].value()==True:                  
                        if orderForm['side'].value() == True:
                            # 2주 + 1끼 + 반찬포함
                            program = Program.objects.get(id=3)                           

                        else:
                            # 2주 + 1끼 + 반찬미포함                            
                            program = Program.objects.get(id=4)                           

                    elif orderForm['twoMeals'].value()==True:                                           
                        if orderForm['side'].value() == True:
                            # 2주 + 2끼 + 반찬포함
                            program = Program.objects.get(id=7)
                        else:
                            # 2주 + 2끼 + 반찬포함
                            program = Program.objects.get(id=8)

                elif orderForm['fourweeks'].value() == True:
                    request.session['week']=4
                    # 4주 식단
                    if orderForm['oneMeal'].value()==True:                                          
                        if orderForm['side'].value() == True:
                            # 4주 + 1끼 + 반찬포함
                            program = Program.objects.get(id=9)
                        else:
                            # 4주 + 1끼 + 반찬미포함
                            program = Program.objects.get(id=5)

                    elif orderForm['twoMeals'].value()==True:                   
                        if orderForm['side'].value() == True:
                            # 4주 + 2끼 + 반찬포함
                            program = Program.objects.get(id=6)   
                        else:
                            # 4주 + 2끼 + 반찬미포함
                            program = Program.objects.get(id=10)


                """
                시작날을 기준으로 단품(Product)의 생산해야할 수량을 업데이트
                """
                product = Product.objects.filter(program=program)
                for p in product:
                    schedule = Schedule.objects.get(product=p)
                    if schedule.date >= d and schedule.date <= d + datetime.timedelta(int(request.session['week'])*7)and schedule.isActive is True:
                        p.toBproduced += int(orderForm['ppl'].value())
                        cart.product.add(p)
                        p.save()
                cart.program.add(program)
                cart.final_price += program.price
                cart.final_price *= int(orderForm['ppl'].value())
                cart.save()
                print("cart: " + str(cart))
                return redirect(orderPage)

            # 비회원
            else:
                member = Member.objects.create()
                member.isRegistered = '0'
                member.save()
                request.session['member'] = member
                cart = Member_cart.objects.create(member=member)
                # 2주
                if orderForm['twoweeks'].value() == True:
                    request.session['week']=2                    
                    if orderForm['oneMeal'].value()==True:
                        if orderForm['side'].value() == True:
                            # 2주 1끼 포함                            
                            program = Program.objects.get(id=3)
                        else:
                            #2주 1끼 미포함
                            program = Program.objects.get(id=4)
                    elif orderForm['twoMeals'].value()==True:                                          
                        if orderForm['side'].value() == True:
                            # 2주 2끼 포함                            
                            program = Program.objects.get(id=7)
                        else:
                            # 2주 2끼 미포함                            
                            program = Program.objects.get(id=8)
                elif orderForm['fourweeks'].value() == True:
                    request.session['week']=4                    
                    if orderForm['oneMeal'].value()==True:                                       
                        if orderForm['side'].value() == True:
                            # 4주 1끼 포함                            
                            program = Program.objects.get(id=9)
                        else:
                            program = Program.objects.get(id=5)
                    elif orderForm['twoMeals'].value()==True:                
                        if orderForm['side'].value() == True:
                            # 4주 2끼 포함
                            program = Program.objects.get(id=6)
                        else:
                            # 4주 2끼 미포함
                            program = Program.objects.get(id=10)
                                
            product = Product.objects.filter(program=program)
            for p in product:
                schedule = Schedule.objects.get(product=p)
                if schedule.date >= d and schedule.date <= d + datetime.timedelta(int(request.session['week'])*7)and schedule.isActive is True:
                    p.toBproduced += int(orderForm['ppl'].value())
                    cart.product.add(p)
                    p.save()                 
            cart.program.add(program)
            cart.final_price += program.price
            cart.final_price *= int(orderForm['ppl'].value())
            request.session['cart'] = cart.id
            cart.save()
            print("go")
            return redirect(orderPage)
                              
    else:
        orderForm = applyForm()
    return render(request,'apply.html', {'orderForm':orderForm})

"""
비회원 주문 조회
"""
def guestOrderHistory(request):
    # 개별 날짜 수정 
    if request.GET.get('change'):
        print("Clikced to change")
        track_id = request.GET['change']
        t_obj = OrderTracking.objects.filter(id=track_id)
        t_obj.delete()

        # date_in_str = 날짜 
        date_in_str = str(request.GET.get('dateData'))
        # Type Casting
        try:
            d = datetime.datetime.strptime(date_in_str, '%Y-%m-%d').date()
        except:
            return HttpResponse("Your date format is wrong")
        tracking = request.session['uuid']
        order = Order.objects.get(uni_id=tracking)
        member = order.member
        # Tracking Object 수정

        added_order = OrderTracking.objects.create(order=order,customer=member,date=d)
        track = OrderTracking.objects.filter(order=order).order_by('date')
        return render(request,'guestOrderHistoryCheck.html',{'order':order, 'tracking':track})
    
    # 주문 조회    
    if request.method == 'POST':
        checkingForm = checkOrderGuest(request.POST)
        if checkingForm.is_valid():
            tracking = checkingForm['uuid'].value()
            request.session['uuid'] = tracking
            print(tracking)
            order = None
            try:
                order = Order.objects.get(uni_id=tracking)
                track = OrderTracking.objects.filter(customer=order.member)
            except:
                return render(request,'guestOrderHistoryNone.html')
            return render(request,'guestOrderHistoryCheck.html',{'order':order, 'tracking':track})
        else:
            return HttpResponse("Form is not valid")    
    else:
        checkingForm = checkOrderGuest()
    return render(request,'guestOrderHistory.html',{'form': checkingForm})

"""
주문페이지 이후 주문정보입력
"""
def orderPage(request):
    if request.method == 'POST':
        shipping_form = shippingForm(request.POST)
        price = Price.objects.create()        
        if shipping_form.is_valid():          
            new_order = shipping_form            
            new_order.save()           
            order_info = Order.objects.create()
            # 16자리 랜덤 주문번호 생성
            order_info.uni_id = get_random_string(length=16).upper()
            
            # 회원가입된 사람이면
            if request.user.is_authenticated():                
                order_info.isMember = True
                profile = Profile.objects.get(user=request.user)                
                member = Member.objects.get(member=profile)
                member_cart_objs = Member_cart.objects.filter(member=member).order_by('-id')
                # 가장 최근의 카트를 가져옴
                member_cart = member_cart_objs[0]
                order_info.cart = member_cart                
                price.final_price += member_cart.final_price              
                order_info.member = member
                
            # 비회원
            else:                
                member = request.session['member']
                member.isRegistered = '0'
                order_info.isMember = False                
                guest_cart = Member_cart.objects.get(id=request.session['cart'])
                guest_cart.member = member
                order_info.cart = guest_cart
                price.final_price += guest_cart.final_price
                order_info.member = member

            # 가장 최근의 object를 가져옴
            order_info.shipping = Shipping_info.objects.latest('id')
            price.save()
            order_info.order_date = timezone.now()
            order_info.price = price
            """
            메테전용 시작
            """
            week = order_info.shipping.duration
            if str(week) == "1주":
                    week = 1
            if str(week) == "2주":
                    week = 2
            days = order_info.shipping.iteration
            if str(days) == "1번":
                    days = 1
            if str(days) == "2번":
                    days = 2
            """
            메테전용 끝
            """
            order_info.toBdelivered = int(request.session['week']) * 2
            order_info.start = request.session['date']
            order_info.save()

            range_index = int(request.session['week']) * 7
            #Type Casting
            d = datetime.datetime.strptime(order_info.start, '%Y-%m-%d').date()
            # 식단 시작일로부터 '수요일', '토요일' 찍음
            for i in range(range_index):
                days = d + datetime.timedelta(i)
                if (days.weekday() == 2) or (days.weekday() == 5):
                    orderTrack = OrderTracking.objects.create(order=order_info,customer=order_info.member,date=days)
                    orderTrack.save()

            return render(request,'order_done.html', {'order_info': order_info})
        else:
            print("Form is not valid ")
            shipping_form = shippingForm()
    else:
        shipping_form = shippingForm()
        print("In this order page " + request.session['date'])
    return render(request, 'order.html', {'shipping_form': shipping_form})

"""
로그인
"""
def ask2Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            user = authenticate(username = cleanedData['username'],
                                password = cleanedData['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Successful Authentication!')
                else:
                    return HttpResponse('This account is disabled')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'ask.html', {'form': form})

"""
회원용 주문 내역
"""
def CheckoutInfo(request):    
    cart = Member_cart.objects.latest('id')
    return render(request, 'orderInfo.html', {'cart':cart})

"""
식단 기간 변경시 기간체크
"""
def changeDuration(request):
    if request.method == 'POST':
        form = durationForm(request.POST)
        """
        start = 이 날 부터 안먹고싶음
        new_start =  이 날 부터 받고싶음
        """
        start = form['from_date'].value()
        new_start = form['new_start'].value()

        order_obj = Order.objects.get(uni_id=request.session['uuid'])
        cart = order_obj.cart       
        week = 0
        period = Program_duration.objects.get(program=cart.program.all())        
        if str(period) == "2주":
            week =2            
        elif str(period) == "4주":
            week=4            

        # Type Casting
        try:
            s_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
            n_date = datetime.datetime.strptime(new_start, '%Y-%m-%d').date()
        except:
            return HttpResponse("Check your dates")
        orderT_obj = OrderTracking.objects.filter(order=order_obj)
        removed = 0

        # 배송 예정 object 제거
        for ot in orderT_obj:
            if ot.date >= s_date and ot.date < n_date:
                print("removed!")
                ot.delete()
                removed += 1
        print("removed: " + str(removed))
        if removed is 0:
            return HttpResponse("There are no meals from " + str(start) + " to " +str(new_start))
        # start = 식단 시작날
        start = order_obj.start
        amount_of_days = week * 7        
        end = start + datetime.timedelta(amount_of_days)        
        count_shipping = 0
        member = order_obj.member
        count = (end-s_date).days
        days_in_the_period = 0;

        """
        안받을 날 부터 원래 식단의 끝날까지 몇번이나 배송(days_in_the_period)을 했어야했나 Count
        """
        for i in range(int(count)):            
            days = s_date + datetime.timedelta(i)
            if (days.weekday() == 2) or (days.weekday() == 5):
                days_in_the_period +=1
        
        i = 0
        if n_date < end:
            n_date = end
        print("########" + str(days_in_the_period))
        """
        새로 받을날부터 새로운 배송 Object 추가
        """

        order_obj = Order.objects.get(uni_id=request.session['uuid'])
        while removed != 0:
            print("i = " + str(i))
            days = n_date + datetime.timedelta(i)
            i += 1            
            if (days.weekday() == 2) or (days.weekday() == 5):              
                if OrderTracking.objects.filter(order=order_obj,customer=member,date=days).exists():
                    print("lol got it -> " + str(days))
                else:
                    orderTrack = OrderTracking.objects.create(order=order_obj,customer=member,date=days)
                    removed -= 1
                    orderTrack.save()
                    print("added ---->" + str(days))

        orderTrack = OrderTracking.objects.filter(order=order_obj,customer=member).order_by('date')
        return render(request,'changedCompleted.html',{'order':order_obj, 'tracking':orderTrack})
    else:
        form = durationForm()
    return render(request,'reschedule.html',{'form':form})
 