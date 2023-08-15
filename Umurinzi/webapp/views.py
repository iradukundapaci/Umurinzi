from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from .models import *
from django.core import serializers
from django.http import JsonResponse



def home(request):
    """ Render Home Page with Found Items"""
    return render(request, "webapp/index.html")


def signup(request):
    """ user signup form
        return:
            home url on success else signup form
    """
    if request.method == "POST":
        form = Signup_form(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile()
            profile.user_id = user
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.tel_no = form.cleaned_data["tel_no"]
            profile.save()
            return redirect("login")
    form = Signup_form()
    return render(request, "webapp/signup.html", {'form':form})


@login_required
def userHome(request):
    """
    this function is used to render the user home page
    containing the user's items 
    """
    items = Item.objects.filter(status="Found").prefetch_related('image_set').all()
    return render(request, "webapp/userHome.html", {"items":items})

@login_required
def registerItem(request):
    """ Register new item"""
    if request.method == "POST":
        id_form = SpecialId_set(request.POST, request.FILES)
        form = UserRegisterItem(request.POST, request.FILES)
        image_form = Image_set(request.POST, request.FILES)
        if form.is_valid() and id_form.is_valid() and image_form.is_valid():
            item = Item(name=form.cleaned_data["name"],
                        description=form.cleaned_data["description"],
                        category=form.cleaned_data["category"],
                        sub_category=form.cleaned_data["sub_category"],
                        brand=form.cleaned_data["brand"],
                        status="OWN",
                       )
            item.owner = request.user
            item.save()
            for form in image_form:
                if form.cleaned_data.get('image'):
                    register_image = Image(item_id=item, image=form.cleaned_data.get('image'))
                    register_image.save()

            for form in id_form:
                if form.cleaned_data.get('number_type'):
                    register_id = SpecialId(item_id=item, number_type=form.cleaned_data.get('number_type'), number_value=form.cleaned_data.get("number_value"))
                    register_id.save()

        else:
            print(form.errors)
            print(id_form.errors)
            print(image_form.errors)
        return redirect("user_home")
    id_form = SpecialId_set(queryset=SpecialId.objects.none())
    form = UserRegisterItem()
    image_form = Image_set(queryset=Image.objects.none())
    return render(request, "webapp/registerNewItem.html", {"id_form":id_form, "form":form, "image_form": image_form})

@login_required
def registerFoundItem(request):
    """report Found Item"""
    if request.method == "POST":
        id_form = SpecialId_set(request.POST, request.FILES)
        form = UserFoundItem(request.POST, request.FILES)
        image_form = Image_set(request.POST, request.FILES)
        if form.is_valid() and id_form.is_valid() and image_form.is_valid():
            print("it is valid")
            item = Item(name=form.cleaned_data["name"],
                        description=form.cleaned_data["description"],
                        category=form.cleaned_data["category"],
                        sub_category=form.cleaned_data["sub_category"],
                        brand=form.cleaned_data["brand"],
                        status="FOUND",
                       )
            item.owner = request.user
            item.save()

            register = Report(item_id=item, province=form.cleaned_data["province"],
                                     sector=form.cleaned_data["sector"], district=form.cleaned_data["district"], report_time=form.cleaned_data["date_time_field"])
            register.save()

            for form in image_form:
                if form.cleaned_data.get('image'):
                    register_image = Image(item_id=item, image=form.cleaned_data.get('image'))
                    register_image.save()

            for form in id_form:
                if form.cleaned_data.get('number_type'):
                    register_id = SpecialId(item_id=item, number_type=form.cleaned_data.get('number_type'), number_value=form.cleaned_data.get("number_value"))
                    register_id.save()

        else:
            print(form.errors)
            print(id_form.errors)
            print(image_form.errors)
        return redirect("user_home")
    id_form = SpecialId_set(queryset=SpecialId.objects.none())
    form = UserFoundItem()
    image_form = Image_set(queryset=Image.objects.none())
    return render(request, "webapp/registerFoundItem.html", {"id_form":id_form, "form":form, "image_form": image_form})


def itemDetail(request, item_id):
    """
        Render Item details
        args:
            item_id: id for the item
        return:
            Html with Item
    """
    item = Item.objects.get(pk=item_id)
    if item is not None:
        images = Image.objects.filter(item_id=item_id)
        return render(request, "webapp/itemView.html", {"item":item, "images":images, })
    else:
        return (404)

def get_categories(request):
    """ Retrieves catagories and subcategories
        return: jsonresponse of categories and their subcategories
    """
    categories = ItemCategory.objects.prefetch_related("subcategory_set").all()
    data = []
    for category in categories:
        subcategories = category.subcategory_set.all()
        category_dict = {
            'id': category.id,
            'name': category.category_name,
            'subcategories': [{'id': sub.id, 'name': sub.sub_category} for sub in subcategories],
        }
        data.append(category_dict)
    return JsonResponse(data, safe=False)

def itemFilter(request, category, subcategory):
    """ Handles Item filter
        agrs:
            category: category of item
            subcategory: subcategory of item
        return:
            jsonResponse: retieved items
    """
    items = Item.objects.filter(category__id=category, sub_category__id=subcategory,status="FOUND").prefetch_related('image_set').all()
    json_obj = []

    for item in items:
        images = item.image_set.all()
        item_dict = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "image": images[0].image.url,
        }
        json_obj.append(item_dict)

    return JsonResponse(json_obj, safe=False)

def retrieveItems(request):
    """ Retrieves Item filter
        return:
            jsonResponse: retieved items
    """
    STATUS = ["FOUND", "LOST"]
    items = Item.objects.filter(status__in=STATUS).prefetch_related('image_set').all()
    json_obj = []

    for item in items:
        images = item.image_set.all()
        item_dict = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "image": images[0].image.url,
        }
        json_obj.append(item_dict)


    return JsonResponse(json_obj, safe=False)

def searchItem(request):
    """ search for Item
        return:
            jsonResponse: retieved items
    """
    if request.method == "POST":
        query = request.POST.get("search_query")
        items = Item.objects.filter(name__icontains=query, status="FOUND").prefetch_related('image_set').all()
        json_obj = []

        for item in items:
            images = item.image_set.all()
            item_dict = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "image": images[0].image.url,
            }
            json_obj.append(item_dict)

        return JsonResponse(json_obj, safe=False)


def check_stolen_item(request):
    """ Validate Item
        return:
            jsonResponse: message
    """
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        category_name = request.POST.get('category_name')
        special_id_value = request.POST.get('special_id_value')

        # Check if the item exists in the LostItem table based on item name, category, and special id.
        if Report.objects.filter(item_id__name=item_name, item_id__category__name=category_name, item_id__specialid__number_value=special_id_value).exists():
            return JsonResponse({"message": "The item is marked as stolen.", "status": "stolen"})
        else:
            return JsonResponse({"message": "The item is not stolen.", "status": "not_stolen"})

    return render(request, "webapp/validateitem.html")

@login_required
def delete_item(request, item_id):
    """ Deletes Item
        return:
            jsonResponse: message
    """
    item = Item.objects.get(pk=item_id)
    if item is not None:
        item.owner = None
        item.status = 'DELETED'
        item.save()
        Report.objects.filter(item_id=item).delete()
        return redirect("user_home")
    else:
        return JsonResponse({"message": "The item is not found.", "status": "not found"})

@login_required
def report_item(request, item_id):
    """ reports Item
        return:
            jsonResponse: message
    """
    item = Item.objects.get(pk=item_id)
    if item is not None:
        item.status = request.POST.get("status")
        item.save()
        report = Report()
        report.item_id = item
        report.province = request.POST.get("province")
        report.district = request.POST.get("district")
        report.sector = request.POST.get("sector")
        report.report_time = request.POST.get("date_time_field")
        report.save()
        return redirect("user_home")
    else:
        return JsonResponse({"message": "The item is not found.", "status": "not found"})
    

@login_required
def update_item(request, item_id):
    """ Update Item
        args:
            id: item id
        return:
            http codes
    """
    instance = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        id_form = SpecialId_set(request.POST, request.FILES)
        form = UserRegisterItem(request.POST, request.FILES)
        image_form = Image_set(request.POST, request.FILES)
        if form.is_valid() and id_form.is_valid() and image_form.is_valid():
            print("valid")
            instance.name = form.cleaned_data["name"]
            instance.description = form.cleaned_data["description"]
            instance.category = form.cleaned_data["category"]
            instance.sub_category = form.cleaned_data["sub_category"]
            instance.brand = brand=form.cleaned_data["brand"]
            instance.save()
            Image.objects.filter(item_id=item_id).delete()
            SpecialId.objects.filter(item_id=item_id).delete()
            for form in image_form:
                if form.cleaned_data.get('image'):
                    register_image = Image(item_id=instance, image=form.cleaned_data.get('image'))
                    register_image.save()

            for form in id_form:
                if form.cleaned_data.get('number_type'):
                    register_id = SpecialId(item_id=instance, number_type=form.cleaned_data.get('number_type'), number_value=form.cleaned_data.get("number_value"))
                    register_id.save()

        else:
            print(form.errors)
            # print(id_form.errors)
            print(image_form.errors)
        return redirect("user_home")
    id_form = SpecialId_set(queryset=SpecialId.objects.none())
    form = UserRegisterItem(instance=instance)
    image_form = Image_set(queryset=Image.objects.filter(item_id=item_id))
    return render(request, "webapp/registerNewItem.html", {"id_form":id_form, "form":form, "image_form": image_form})
