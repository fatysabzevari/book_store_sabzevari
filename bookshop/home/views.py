from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'home/home.html')

def all_product(request):
    return render(request, 'home/product.html')