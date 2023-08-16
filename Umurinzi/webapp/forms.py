from django.forms.models import inlineformset_factory
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class Signup_form(UserCreationForm):
    first_name  = forms.CharField(label="", min_length=2)
    last_name   = forms.CharField(label="", required=False)
    tel_no      = forms.CharField(label="", min_length=10, max_length=12)
    user_id     = forms.CharField(label="", min_length=16, max_length=16)
    class Meta(UserCreationForm):
        model   = User
        fields  = ["user_id", "first_name", "last_name", "tel_no"]


class SpecialIDForm(forms.ModelForm):
    number_value      = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder":"Number"}))
    class Meta:
        model = SpecialId
        fields = ['number_type', 'number_value']

SpecialId_set = forms.modelformset_factory(SpecialId, form=SpecialIDForm, extra=3, max_num=3)
updateId_set = forms.modelformset_factory(SpecialId, form=SpecialIDForm, extra=3, max_num=3, validate_max=False, validate_min=False, can_delete=True)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]

Image_set = forms.modelformset_factory(Image, fields=["image"], extra=3, max_num=3)
updateImage_set = forms.modelformset_factory(Image, fields=["image"], extra=3, max_num=3, validate_max=False, validate_min=False, can_delete=True)

class UserRegisterItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "category", "sub_category", "brand" ]

class UserFoundItem(forms.ModelForm):
    province = forms.CharField(label="", max_length=50, widget=forms.Select(), required=True)
    sector   = forms.CharField(label="", max_length=50, widget=forms.Select(), required=True)
    district = forms.CharField(label="", max_length=50, widget=forms.Select(), required=True)
    date_time_field = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type":"datetime-local"}))
    class Meta:
        model = Item
        fields = ["name", "description", "category", "sub_category", "brand", "province", "district", "sector", "date_time_field" ]

class ValidateItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "category", "sub_category", "brand"]