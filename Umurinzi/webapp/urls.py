from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path("", home, name="user_home"),
    path("login", LoginView.as_view(template_name='webapp/login.html'), name="login"),
    path("logout",LogoutView.as_view(), name="logout"),
    path("signup", signup, name="signup"),
    path("item/<int:item_id>", itemDetail, name="item_details"),
    path("registeritem", registerItem, name="register_new_item"),
    path("manageitems", manageItems, name="manage_item"),
    path("reportfound", registerFoundItem, name="register_found_item"),
    path("get_categories/", get_categories, name='get_categories'),
    path("filter/<int:category>/<int:subcategory>/", itemFilter, name="filter_items"),
    path("items/", retrieveItems, name="items"),
    path("registereditems/", retrieveRegisteredItems, name="registered_items"),
    path("itemsearch/", searchItem, name="item_serach"),
    path("item/report/<int:item_id>", report_item, name="item_report"),
    path("item/delete/<int:item_id>", delete_item, name="item_delete"),
    path("item/update/<int:item_id>", update_item, name="item_update"),
    path("claimitem/<int:item_id>", claim_item, name="claim_item"),
    path('validateitem/', validateItem, name='validate_item'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
