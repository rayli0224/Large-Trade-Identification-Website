from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from .models import User, Stock
from django.views.decorators.csrf import csrf_exempt
import json

from . import large_trade_identifier as lt
from . import email

def index(request):
    if 'logged_in' in request.session and request.session['logged_in'] == True:
        print(request.session['logged_in'])
        return HttpResponse("This is a test response to show that the user is logged in")
    return HttpResponse("The user is not logged in")
def create_user(request):
    print("doing nothing for now")

@csrf_exempt

def changepass(request):
    if request.method == 'POST':
        print("this is true")
        if 'logged_in' in request.session and request.session['logged_in'] == True:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            if body['password'] == body['passwordconf']:
                user = User.objects.get(user_name = request.session['user_name'], password = request.session['password'])
                user.password = body['password']
                request.session['password'] = body['password']
                user.save()
                return JsonResponse({'success':'True'})
    return JsonResponse({'success':'False'})

@csrf_exempt

def removestock(request):
    if request.method == 'POST':
        print("remove stock is true")
        if 'logged_in' in request.session and request.session['logged_in'] == True:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            Stock.objects.get(email=body['email'], stock_ticker=body['stock']).delete()
            return JsonResponse({'success':'True'})
    return JsonResponse({'success':'False'})

@csrf_exempt

def get_profile(request):
    print("this is running ")
    if request.method == 'GET':
        print("this is true")
        print(request.session['logged_in'])
        if 'logged_in' in request.session and request.session['logged_in'] == True:
            return JsonResponse({'user_name': request.session['user_name'], 'password': request.session['password'], 'email': request.session['email'], 'failed':'False'})
        return JsonResponse({'failed': 'True'})
    else:
        return JsonResponse({'failed': 'True'})

@csrf_exempt

def get_stocks(request):
    print("get stocks is running ")
    if request.method == 'GET':
        print("this is true")
        print(request.session['logged_in'])
        if 'logged_in' in request.session and request.session['logged_in'] == True:
            stock_entries = Stock.objects.all().filter(email=request.session['email'])
            stocks = []
            for entry in stock_entries:
                print("entry: ", entry.stock_ticker)
                print("entry type: ", type(entry.stock_ticker))
                stocks.append(entry.stock_ticker)
            return JsonResponse({'stocks': stocks, 'email': request.session['email'], 'failed':'False'})
        return JsonResponse({'failed': 'True'})
    else:
        return JsonResponse({'failed': 'True'})

@csrf_exempt

def notify_users():
    stocks_and_emails = Stock.objects.all()
    print(len(stocks_and_emails))
    print("this is being called")
    for entry in stocks_and_emails: 
        ticker = entry.stock_ticker
        email_entry = entry.email
        print("ticker: ", ticker)
        print("email entry: ", email_entry)
        print("loading data: ")
        large_trades_JSON, large_trades_CSV = lt.get_large_trades(ticker)
        print("final json: ")
        print(large_trades_JSON)
        print("sending email: ")
        email.send_json_email(large_trades_JSON, [email_entry], ticker)
        print("finished email send")

@csrf_exempt

def notify_user(request):
    stocks_and_emails = Stock.objects.all().filter(email=request.session['email'])
    print("this is being called")
    for entry in stocks_and_emails: 
        ticker = entry.stock_ticker
        email_entry = entry.email
        print("ticker: ", ticker)
        print("email entry: ", email_entry)
        print("loading data: ")
        large_trades_JSON, large_trades_CSV = lt.get_large_trades(ticker)
        print("final json: ")
        print(large_trades_JSON)
        print("sending email: ")
        email.send_json_email(large_trades_JSON, [email_entry], ticker)
        print("finished email send")

@csrf_exempt
def add_stock(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if request.method == 'POST' and request.session['logged_in'] == True:
        stock = body['stock']
        try:
            stock = Stock.objects.get(email = request.session['email'], stock_ticker = stock) # check if stock already exists
            print("stock already exists")
        except:
            Stock.objects.create(email = request.session['email'], stock_ticker = stock)
            print("successfully started tracaking the stock: ", stock, " for user: ", request.session['email'])
        # do something here
        notify_user(request) # place holder
        # get response, perhaps JSON format?  
        return JsonResponse({}, safe=False)
    return JsonResponse({})

@csrf_exempt
def signup(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if request.method == 'POST':
        user_name_req = body['user_name']
        password_req = body['password']
        passwordconf_req = body['passwordconf']
        email_req = body['email']
        if password_req == passwordconf_req:
            try: 
                print("this is being called")
                print("username: ", user_name_req)
                print("password: ", password_req)
                user = User.objects.get(user_name = user_name_req, password = password_req) # check if user already exists
                print("logged in successfully")
                request.session['logged_in'] = True    
                return JsonResponse({'logged_in':'True'})
            except:
                try:
                    print("this is being called instead")
                    User.objects.create(user_name = user_name_req, password = password_req, email = email_req)
                    request.session['logged_in'] = True 
                    request.session['user_name'] = user.user_name
                    request.session['password'] = user.password
                    request.session['email'] = user.email   
                    return JsonResponse({'logged_in':'True'})
                except:
                    print("this exception was thrown")
                    request.session['logged_in'] = False
                    return JsonResponse({'logged_in':'False'})
    request.session['logged_in'] = False
    return JsonResponse({'logged_in':'False'})


@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_name = body['user_name']
    if request.method == 'POST':
        user_name_req = body['user_name']
        password_req = body['password']
        print(user_name_req)
        try:
            user = User.objects.get(user_name = user_name_req, password = password_req)
            request.session['logged_in'] = True
            request.session['user_name'] = user.user_name
            request.session['password'] = user.password
            request.session['email'] = user.email
            print(user)
            return JsonResponse({'logged_in':'True'})
        except:
            request.session['logged_in'] = False
            return JsonResponse({'logged_in':'False'})
    request.session['logged_in'] = False
    return JsonResponse({'logged_in':'False'})