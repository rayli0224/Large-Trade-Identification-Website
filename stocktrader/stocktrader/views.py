from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
def home(request):
    return render(request, 'login.html')

def search(request):
    if 'logged_in' in request.session and request.session['logged_in'] == True:
        return render(request, 'search.html')
    else:
        return render(request, 'login.html')
    
def signup(request):
    if 'logged_in' in request.session and request.session['logged_in'] == True:
        return render(request, 'search.html')
    else:
        return render(request, 'signup.html')
    
def profile(request):
    return render(request, 'userProfile.html')
