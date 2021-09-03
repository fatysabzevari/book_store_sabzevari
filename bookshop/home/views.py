from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Q
from cart.models import *


# Create your views here.
def home(request):
    category = Category.objects.all()    #از داخل دیتابیس همه دسته بندی هارا بگیرد
    return render(request,'home/home.html', {'category': category})

def all_product(request, slug=None, id=None):
    products = Product.objects.all()
    form = SearchForm()
    category  = Category.objects.all()
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data['search']
            products = products.filter(Q(name__contains=data))
    if slug and id:
        data = get_object_or_404(Category,slug=slug,id=id)
        products = products.filter(category=data)
    return render(request, 'home/product.html', {'products':products, 'category':category,'form':form})

def product_detail(request,id):
    product = get_object_or_404(Product,id=id)  #بر اساس ای دی تفکیک میکنیم

    cart_form = CartForm()
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    if product.status != 'None':
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
        context = {'product':product,'variant':variant,'variants':variants,'is_like':is_like ,'is_unlike':is_unlike,'cart_form':cart_form}
        return render(request,'home/detail.html',context )
    else:
        # return render(request, 'home/detail.html', {'product': product})
        return render(request,'home/detail.html',{'product':product,'is_like':is_like ,'is_unlike':is_unlike,'cart_form':cart_form})

def get_writer(request, id):
    wrt = get_object_or_404(Writer, id=id)
    product = Product.objects.filter(writer_id=wrt.id)
    context = {
        "wrt": wrt,
        "product": product
    }
    return render(request, "home/writer.html", context)



def product_like(request,id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product, id=id)
    is_like =False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
        messages.success(request, 'remove', 'success')
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request,'add','warning')
    return redirect(url)


def product_unlike(request,id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product, id=id)
    product.unlike.add(request.user)
    # is_unlike =False
    # if product.unlike.filter(id=request.user.id).exists():
    #     product.unlike.remove(request.user)
    #     is_unlike = False
    #     messages.success(request, 'remove like', 'danger')
    # else:
    #     product.unlike.add(request.user)
    #     is_unlike = True
    messages.success(request,'add like','dark')
    return redirect(url)


def product_search(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit() :
                products = products.filter(Q(discount__exact=data)|Q(unit_price__exact=data))           #محصولاتی را برای من بیار که اسم محصول برابر با دیتا باشد(چیزی که کاربر سرچ کرده است) استفاده از فیلد لوک آپ
            else:
                products = products.filter(Q(name__contains=data)) #بر اساس 3 ویژگی محصول،قیمت،تخفیف سرچ میکند
            return render(request,'home/product.html',{'products':products,'form':form})
