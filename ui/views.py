from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from . import models

# Create your views here.

def signup(request):
    return render(request,"signup.html")

def loadBase(request,context):
    categories = models.Category.objects.all()
    mainCategories = categories[:min(4, len(categories))]
    extraCategories = categories[min(4, len(categories)):len(categories)]

    username = "Login"

    if request.user.is_authenticated:
        username = request.user.username

    value = context | {
        'mainCategories': mainCategories,
        'extraCategories': extraCategories,
        'username': username
    }
    return value

def index(request):
    best_seller_items = models.Product.objects.filter(isBestSeller=True)
    best_seller_items = best_seller_items[:min(5, len(best_seller_items))]
    espresso_machines = models.Product.objects.filter(subcategory__title__icontains='espresso machines')
    espresso_machines = espresso_machines[:min(4, len(espresso_machines))]
    cooking_equipment = models.Product.objects.filter(subcategory__title__icontains='cooking equipment')
    cooking_equipment = cooking_equipment[:min(4, len(cooking_equipment))]
    refrigerators = models.Product.objects.filter(subcategory__title__icontains='refrigerator')
    refrigerators = refrigerators[:min(5, len(refrigerators))]
    context = {
        'bestSellerItems': [{
            'title': item.title,
            'rating': item.rating()['rating'],
            'reviewCount': item.rating()['count'],
            'price': item.price,
            'mainImage': item.mainImage
        } for item in best_seller_items],
        'espressoMachines': [{
            'title': item.title,
            'rating': item.rating()['rating'],
            'reviewCount': item.rating()['count'],
            'price': item.price,
            'mainImage': item.mainImage
        } for item in espresso_machines],
        'cookingEquipment': [{
            'title': item.title,
            'rating': item.rating()['rating'],
            'reviewCount': item.rating()['count'],
            'price': item.price,
            'mainImage': item.mainImage
        } for item in cooking_equipment],
        'refrigerators': [{
            'title': item.title,
            'rating': item.rating()['rating'],
            'reviewCount': item.rating()['count'],
            'price': item.price,
            'mainImage': item.mainImage
        } for item in refrigerators],
    }
    return render(request, 'index.html', loadBase(request, context))

def signup(request, fail = 0):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'signup.html')

def createuser(request):
    username = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['cpassword']
    if confirm != password:
        return redirect(signup, fail=1)
    user = models.User(username=username, email=username, first_name=request.POST['fname'], last_name=request.POST['lname'])
    user.set_password(password)
    user.save()
    login(request, user)
    return redirect('/')

def cart(request):
    context = {}
    return render(request, "cart.html", context=context)

def category(request, id):
    category = models.Category.objects.get(id=id)
    subcategories = list(models.Subcategory.objects.filter(category=category))
    context = {
        "category" : {
            "title" : category.title,
            "image" : category.mainImage,
        },
        "subcategories": [
            {
                "title" : item.title,
                "image" : item.image,
            }
            for item in subcategories
        ],
    }
    return render(request, "category.html", context)

def checkout(request):
    context = {}
    return render(request, "checkout.html", context)

def loginPage(request, displayErrorMessage = False):
    errorMessageBool = False
    if displayErrorMessage:
        errorMessageBool = True
        
    context = {
        'displayErrorMessage': errorMessageBool
    }

    return render(request, 'login.html', context)

def products(request):
    return render(request, 'products.html')

def auth(request):
    if request.POST['email'] and request.POST['pass']:
        user = authenticate(request, username=request.POST['email'], password=request.POST['pass'])
        if user:
            login(request, user)
            return redirect('/')
    return redirect('/login/1/')