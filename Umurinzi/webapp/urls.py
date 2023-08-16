from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login", LoginView.as_view(template_name='webapp/login.html'), name="login"),
    path("logout",LogoutView.as_view(), name="logout"),
    path("signup", signup, name="signup"),
    path("userhome", userHome, name="user_home"),
    path("item/<int:item_id>", itemDetail, name="item_details"),
    path("userhome/registeritem", registerItem, name="register_new_item"),
    path("userhome/reportfound", registerFoundItem, name="register_found_item"),
    path("get_categories/", get_categories, name='get_categories'),
    path("filter/<int:category>/<int:subcategory>/", itemFilter, name="filter_items"),
    path("items/", retrieveItems, name="items"),
    path("itemsearch/", searchItem, name="item_serach"),
    path("userhome/item/report/<int:item_id>", report_item, name="item_report"),
    path("userhome/item/delete/<int:item_id>", delete_item, name="item_delete"),
    path("userhome/item/update/<int:item_id>", update_item, name="item_update"),
    path("claimitem/<int:item_id>", claim_item, name="claim_item"),
    path('validateitem/', validateItem, name='validate_item'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
