from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import HttpResponseRedirect
from .models import product
from django.contrib import messages
from twilio.rest import Client
from django.core.mail import send_mail
from mainapp.settings import EMAIL_HOST_USER

# Create your views here.
# page redirections here


def home(request):
    data = product.objects.all()[:10]
    
    return render(request, 'home-page.html',{'data':data})


def category(request):
    data = product.objects.all()

    return render(request, 'categories.html', {'data': data,'errorl': 'Please Login TO Purchase'})


def registration_page(request):
    return render(request, 'register-user.html')


def login_page(request):
    return render(request, 'login.html')
    

def cart_page(request):
    
    return render(request,'cartpage.html')
    
# user authentication


def save_data(request):
    if request.method == 'POST':
        user_name = request.POST['first_name']
        # last_name = request.POST['Last_name']
        # username=first_name+last_name
        number = request.POST['mobile']
        username = request.POST['email']
        address = request.POST['address']
        password1 = request.POST['password']
        password2 = request.POST['comfirm_password']
        # print(first_name,last_name,number,email,address,password1)
        if password1 == password2:
            if User.objects.filter(email=user_name).exists():
                # print("Email is already exist")
                # return render(request, 'home-page.html')
                return render(request, 'register-user.html', {'erroru': 'Username is already taken'})
            # elif number_check==10 :
            #     print("test pass the number is int and length is 10")

            #     return render(request,'register-user.html',{'errorn':'check your mobile number '})
            elif User.objects.filter(username=username).exists():
                # print("username is already exist")
                return render(request, 'register-user.html', {'errore': 'Email is already taken'})

            else:
                # return test(request, username, email, password1)
                user = User.objects.create_user(
                    username=username, first_name=address, last_name=number, email=user_name, password=password1)

                user.save()
                return render(request, 'login.html')
                # return render(request, 'home-page.html')

        else:
            # print("password is not matching")
            return render(request, 'register-user.html', {'errorp': 'Please Check Your Password'})


def Login(request):

    username = request.POST['email_login']
    password = request.POST['password_1']
    # print(email_log,password_log)
    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        # print("user logged in successfully")
        return redirect( '/' )
    else:
        # print("invalid credentials")
       return render(request, 'login.html', {'error': 'Email or Password is incorrect'})
       

def Logout(request):
    logout(request)
    return redirect('/')
# cart


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    data = product.objects.get(id=id)
    cart.add(product=data)

    return redirect('/categories')

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    data = product.objects.get(id=id)
    cart.remove(product=data)
   
    return redirect('/cart/')


@login_required(login_url="/users/login")
def cart_total_amount(request):
	if request.user.is_authenticated:
        
		cart = Cart(request)
		total_bill = 0.0
		for key, value in request.session['cart'].items():
			total_bill = total_bill + (float(value['price']) * value['quantity'])
            
		return {'cart_total_amount': total_bill}
	else:
		return {'cart_total_amount': 0}
@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    data = product.objects.get(id=id)
    cart.add(product=data)
   
    return redirect("/cart/")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    data= product.objects.get(id=id)
    for key, value in request.session['cart'].items():
        if key == str(data.id):

            value['quantity'] = value['quantity'] - 1
            if(value['quantity']< 1 ):
                return redirect('/cart/')
            cart.save()
            break
        else:
            print("Something Wrong")
    
    return redirect("/cart/")


# @login_required(login_url="/users/login")
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("/cart/")


# @login_required(login_url="/users/login")
# def cart_detail(request):
#     return render(request, 'cartpage.html')



# invoice bill for purchased order

@login_required(login_url="/users/login")
def invoice(request):
    if request.user.is_authenticated:
        customer_name=request.user.email
        customer_email=request.user.username
        customer_number=request.user.last_name
        customer_address =  request.user.first_name
        print(customer_name)
        print(customer_email)
        print(customer_number)
        cart = Cart(request)
        summery_list = {}
        total_bill = 0.0
        for key, value in request.session['cart'].items():
            product_name=value['name']
            summery_list['product_name'] = product_name
            print(product_name)
            product_price= value['price']
            summery_list['product_price'] = product_price

            print(product_price)
            product_quantity= value['quantity']
            summery_list['product_quantity'] = product_quantity
            print(product_quantity)
            total_bill = total_bill + (float(value['price']) * value['quantity'])
            summery_list['total_bill'] = total_bill
            total_amount= total_bill
            print(total_amount)
            # summery = [customer_name, customer_email, customer_number, product_name, product_quantity, product_quantity, total_amount]
            # summery1=[summery]
        for data in summery_list:
            data= data
            p_name=summery_list['product_name']
            p_price =summery_list['product_price']
            p_quantity=summery_list['product_quantity']
            p_total=summery_list['total_bill']
    else:
        print("user not found")
    return render(request,'summery.html',)

# order placed email from user to admi


@login_required(login_url="/users/login")
def mail_confirm(request):
    if request.user.is_authenticated:
        customer_name = request.user.email
        customer_email = request.user.username
        customer_number = request.user.last_name
        customer_address = request.user.first_name
        cart = Cart(request)
        summery_list = {}
        total_bill = 0.0
    
        for key, value in request.session['cart'].items():
            product_name = value['name']
            summery_list['product_name'] = product_name
        
            product_price = value['price']
            summery_list['product_price'] = product_price


            product_quantity = value['quantity']
            summery_list['product_quantity'] = product_quantity
            
            total_bill = total_bill + (float(value['price']) * value['quantity'])
            summery_list['total_bill'] = total_bill
            total_amount = total_bill
            # send_mail("order confirmed", "testing ",'satyaambati5@gmail.com',['mailb2331@gmail.com'], fail_silently=True)
        

        
    else:
        print("user not found")

    recipient_list = ['satyaambati5@gmail.com','b','suhanashunnu123@gmail.com']

    send_mail("order confirmed","\n Name:"+ customer_name +"\nemail:" +customer_email,
                'satyaambati5@gmail.com', recipient_list)
   

    return render(request,'success.html' )
    # email_from = email
    # # settings.EMAIL_HOST_USER
    # recipient_list = ['ambatisathya123@gmail.com', ]
    # send_mail(name, message, email_from, recipient_list)

    # return render(request, "index.html")
