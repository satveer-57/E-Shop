from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from random import randrange
from django.conf import settings
from django.core.mail import send_mail
from eshop.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET
import razorpay



def home(Request):
    data = Product.objects.all().order_by('id').reverse()[:8]

    return render(Request, "index.html", {'data': data})


def shop(Request, mc, sc, br):
    if mc == "All" and sc == "All" and br == "All":
        data = Product.objects.all().order_by('id').reverse()
    elif mc != "All" and sc == "All" and br == "All":
        data = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc))
    elif mc == "All" and sc != "All" and br == "All":
        data = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc))
    elif mc == "All" and sc == 'All' and br != 'All':
        data = Product.objects.filter(brand=Brand.objects.get(name=br))
    elif mc != "All" and sc != 'All' and br == 'All':
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc))
    elif mc != "All" and sc == 'All' and br != 'All':
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), brand=Brand.objects.get(name=br))
    elif mc == 'All' and sc != 'All' and br != 'All':
        data = Product.objects.filter(subcategory=Subcategory.objects.get(
            name=sc), brand=Brand.objects.get(name=br))
    else:
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc), brand=Brand.objects.get(name=br))
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    return render(Request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': mc, 'sc': sc, 'br': br})


def singleProduct(Request, id):
    data = Product.objects.get(id=id)
    return render(Request, "single-product.html", {'data': data})


def loginPage(Request):
    if Request.method == 'POST':
        username = Request.POST.get('username')
        password = Request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(Request, user)
            return redirect('/profile')
        else:
            messages.error(Request, "Invalid Username or Password")
    return render(Request, "login.html")


def logoutPage(Request):
    logout(Request)
    return redirect('/login/')


def signupPage(Request):
    if Request.method == 'POST':
        p = Request.POST.get('password')
        cp = Request.POST.get('cpassword')
        if p == cp:
            b = Buyer()
            b.name = Request.POST.get('name')
            b.username = Request.POST.get('username')
            b.email = Request.POST.get('email')
            b.phone = Request.POST.get('phone')
            user = User(username=b.username, email=b.email)
            user.set_password(p)
            try:
                user.save()
                b.save()
                subject = "Your Account is Created  : Team Eshop"
                message = ' Hello '+str(b.name)+"\nThanks to Create a Buyer Account with us\nNow You can Buy Our Latest Products:\nTeam Eshop"
                recipient_list = [b.email]
                email_from=settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from,recipient_list)
                return redirect("/login/")
            except:
                messages.error(Request, "Username Already Taken ....")
        else:
            messages.error(
                Request, "Password and Confirm Password Doesn't Matched ....")
    return render(Request, "signup.html")


@login_required(login_url='/login')
def profilePage(Request):
    user = User.objects.get(username=Request.user)
    if user.is_superuser:
        return redirect('/admin/')
    else:
        buyer = Buyer.objects.get(username=user.username)
        wishlist = Wishlist.objects.filter(user=buyer)
        orders = Checkout.objects.filter(user=buyer)
    return render(Request, "profile.html", {'user': buyer, 'wishlist': wishlist, 'orders': orders})


@login_required(login_url="/login")
def updateProfilePage(Request):
    if Request.user.is_superuser:
        return redirect("/admin")
    else:
        buyer = Buyer.objects.get(username=Request.user.username)
        if Request.method == 'POST':
            buyer.name = Request.POST.get("name")
            buyer.email = Request.POST.get("email")
            buyer.phone = Request.POST.get("phone")
            buyer.addressline1 = Request.POST.get("addressline1")
            buyer.addressline2 = Request.POST.get("addressline2")
            buyer.addressline3 = Request.POST.get("addressline3")
            buyer.pin = Request.POST.get("pin")
            buyer.city = Request.POST.get("city")
            buyer.state = Request.POST.get("state")
            print(Request.FILES.get('pic'), "\n\n\n\n")
            if (Request.FILES.get('pic')):
                buyer.pic = Request.FILES.get("pic")
            buyer.save()
            return redirect("/profile")
        return render(Request, "update-profile.html", {'user': buyer})


def addToCart(Request, id):
    cart = Request.session.get('cart')
    p = Product.objects.get(id=id)
    if cart:
        if str(id) in cart:
            cart[str(id)]['qty'] += 1
            cart[str(id)]['total'] += cart[str(id)]['price']
        else:
            cart.setdefault(str(p.id), {'name': p.name, 'pic': p.pic1.url, 'color': p.color, 'size': p.size, 'price': p.finalprice, 'qty': 1,
                            'total': p.finalprice, 'maincategory': p.maincategory.name, 'subcategory': p.subcategory.name, 'brand': p.brand.name})
            print(cart, "veer")
    else:
        cart = {str(p.id): {'name': p.name, 'pic': p.pic1.url, 'color': p.color, 'size': p.size, 'price': p.finalprice, 'qty': 1,
                    'total': p.finalprice, 'maincategory': p.maincategory.name, 'subcategory': p.subcategory.name, 'brand': p.brand.name}}
    Request.session['cart'] = cart
    Request.session.set_expiry(60*60*60*24)
    return redirect("/cart-page")


def cartPage(Request):
    cart = Request.session.get('cart')
    shipping = 0
    total = 0
    final=0
    if cart is None:
        cart = {}
    else:
        for value in cart.values():
            total += value['total']
        if total <= 1000:
            shipping = 150
        final = shipping+total
    return render(Request, 'cart.html', {'cart': cart, 'total': total, 'shipping': shipping, 'final': final})


def deleteCart(Request, id):
    cart = Request.session.get('cart')
    print(cart)
    if str(id) in cart:
        cart.pop(str(id))
        Request.session['cart'] = cart
    return redirect('/cart-page')


def updateCart(Request, id, action):
    cart = Request.session.get('cart')
    if str(id) in cart:
        if action == 'inc':
            cart[str(id)]['qty'] += 1
            cart[str(id)]['total'] += cart[str(id)]['price']
        elif action == 'dec' and cart[str(id)]['qty'] > 1:
            cart[str(id)]['qty'] -= 1
            cart[str(id)]['total'] -= cart[str(id)]['price']
        Request.session['cart'] = cart
    return redirect('/cart-page')


@login_required(login_url='/login')
def addToWishlist(Request, pid):
    try:
        user = Buyer.objects.get(username=Request.user.username)
        product = Product.objects.get(id=pid)
        try:
            wishlist = Wishlist.objects.get(user=user, product=product)
        except:
            w = Wishlist()
            w.user = user
            w.product = product
            w.save()
        return redirect('/profile')
    except:
        return redirect('/admin')


def deleteWishlist(Request, id):
    print(id, "\n\n\n")
    wishlist = Wishlist.objects.get(id=id)
    wishlist.delete()
    return redirect("/profile")


@login_required(login_url='/login')
def checkOut(Request):
    cart = Request.session.get('cart')
    shipping = 0
    total = 0
    for i in cart.values():
        total += i['total']
    if total < 1000:
        shipping = 150
    final = shipping+total
    try:
        user = Buyer.objects.get(username=Request.user.username)
        return render(Request, 'checkout.html', {'user': user, 'cart': cart, 'shipping': shipping, 'total': total, 'final': final})
    except:
        return redirect('/admin')

client=razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
@login_required(login_url='/login')
def orderPage(Request):
    if Request.method == "POST":
            user = Buyer.objects.get(username=Request.user.username)
            cart = Request.session.get('cart')
            if cart:
                total = 0
                shipping = 0
                check = Checkout()
                check.user = user
                for i in cart:
                    total += cart[i]['total']
                if total < 1000 and total > 0:
                    shipping = 150
                final = shipping+total
                check.shipping = shipping
                check.total = total
                check.final = final
                check.save()
                for i in cart:
                    cp = CheckoutProducts()
                    cp.checkout = check
                    cp.qty = cart[str(i)]['qty']
                    cp.total = cart[str(i)]['total']
                    cp.product = Product.objects.get(id=i)
                    cp.save()
                subject = "Your Order has been Placed : Team Eshop"
                message = 'Hello'+str(user.name)+"\n Thanks to Shop with us.\nNow You can Track Your Order on Profile Page\nTeam Eshop"
                recipient_list = [user.email]
                email_from=settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from,recipient_list)
                Request.session['cart'] = {}
                if Request.POST.get('mode')!='COD':    
                    orderAmount=check.final*100
                    orderCurrency="INR"
                    paymentOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                    paymentId=paymentOrder['id']
                    check.mode=1
                    check.save()
                    return render(Request,'pay.html',{'amount':orderAmount,'api_key':RAZOR_KEY_ID,'order_id':paymentId,'User':user})
                return redirect('/confirmation') 
            else:
                return redirect('/cart-page')
    else:
        return redirect('/check-out')
        
@login_required(login_url='/login/')
def paymentSuccess(Request,rppid,rpoid,rpsid):
    buyer=Buyer.objects.get(username=Request.user)
    check=Checkout.objects.filter(buyer=buyer)
    check=check[-1]
    check.rppid=rppid
    check.status=1
    check.save()
    return redirect('/confirmation/')

@login_required(login_url='/login')
def confirmationPage(Request):
    return render(Request, 'confirmation.html')


def contactPage(Request):
    if Request.method == "POST":
        contact = Contact()
        contact.name = Request.POST.get('name')
        contact.email = Request.POST.get('email')
        contact.phone = Request.POST.get('phone')
        contact.subject = Request.POST.get('subject')
        contact.message = Request.POST.get('message')
        contact.save()
        messages.success(
            Request, "Thanks to Share Your Query with US!! Our Team will contact soon You")
    return render(Request, 'contact.html')


def searchPage(Request):
    if Request.method == "POST":
        print("post\n\n\n\n")
        maincategory = Maincategory.objects.all()
        subcategory = Subcategory.objects.all()
        brand = Brand.objects.all()
        search = Request.POST.get('search')
        print(search, "\n\n\n")
        data = Product.objects.filter(Q(name__icontains=search) | Q(color__icontains=search) | Q(
            stock__icontains=search) | Q(description__contains=search))
    return render(Request, 'shop.html', {'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'data': data, 'mc': 'All', 'sc': 'All', 'br': 'All'})


def forgetUsername(Request):
    if Request.method == "POST":
        username = Request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                redirect('/admin')
            else:
                buyer = Buyer.objects.get(username=username)
                Request.session['resetusername']=username
                otp = randrange(10000, 99999)
                buyer.otp = otp
                buyer.save()
                subject = "OTP for Password Reset  : Team Eshop"
                message = ' OTP for Password Reset is '+str(otp)+"\nTeam Eshop"
                recipient_list = [buyer.email]
                email_from=settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from,recipient_list)
                return redirect('/enter-otp')
        except:
            messages.error(Request,'Invalid Username "Try to put valid Username" ')
    return render(Request, 'forget-username.html')

def enterOtp(Request):
    if Request.method=="POST":
        otp=Request.POST.get('otp')
        try:
            user=Buyer.objects.get(username=Request.session.get('resetusername'))
            if user.otp==int(otp):
                return redirect('/forget-password')
            else:
                messages.error(Request,"Invalid OTP")
        except:
            messages.error(Request,"Unauthorized User")
    return render(Request,'enter-otp.html')

def forgetPassword(Request):
    if Request.method=="POST":
        p=Request.POST.get('password')
        cp=Request.POST.get('cpassword')
        if p==cp:
            user=User.objects.get(username=Request.session.get('resetusername'))
            user.set_password(p)
            user.save()
            return redirect('/login')
        else:
            messages.error(Request,"Your Password and Confirm Password not matched")
    return render(Request,'forget-password.html')


