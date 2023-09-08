from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
    

class CustomUserManager(BaseUserManager):
    """ Model for custom User Manager"""
    def create_user(self,user_id, password=None, **extra_fields):
        """ create user
            args:
                user_id: user id
                password: user password
                extra fields: more options
            return:
                user instance
        """
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        """ create superuser
            args:
                user_id: user id
                password: user password
                extra fields: more options
            return:
                create_user(user_id, password, **extra_fields)
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Model for custom User"""
    user_id = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class UserProfile(models.Model):
    """ Model for Userprofile"""
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    tel_no = models.CharField(max_length=12)

    def __str__(self)->str:
        """ Model string representation"""
        return (self.first_name +" "+ self.last_name)

    def get_short_name(self)->str:
        """ get user short name"""
        return (self.first_name)

      
class Item(models.Model):
    """ Model for Item"""
    brand_choices = [('SAMSUNG', 'SAMSUNG'),('TECNO','TECNO'), ('IPHONE','IPHONE'), ('HP', 'HP'), ('ITEL','ITEL'), ('OTHER', 'OTHER')]
    status_choice = [("OWN", "Own"), ('LOST', 'Lost'), ('FOUND', 'Found'), ('STOLEN', 'Stolen'), ('PENDING', 'Pending'), ('DELETED', 'Deleted')]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    category = models.ForeignKey("ItemCategory", on_delete=models.DO_NOTHING)
    sub_category = models.ForeignKey("SubCategory", on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=100, choices=brand_choices)
    status = models.CharField(max_length=10, choices=status_choice)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, null=True) 

    def __str__(self) -> str:
        """ Model string representation"""
        return self.name
   

class Image(models.Model):
    """ Model for Item Images"""
    item_id = models.ForeignKey("Item", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        """ Model string representation"""
        return str(self.image)
    
class SpecialId(models.Model):
    """ Model for Item identifying numbers"""
    types = [("SN", "Serial Number"),
             ("IMEI", "IMEI"),
             ("CN", "Card Number"),
             ("MAC", "MAC Address")
            ]
    item_id = models.ForeignKey("Item", on_delete=models.CASCADE) 
    number_type = models.CharField(max_length=100, choices=types)
    number_value = models.CharField(max_length=100)

    def __str__(self) -> str:
        """ Model string replesantation"""
        return self.item_id.name + ' ' +self.number_type

class ItemCategory(models.Model):
    """ Model for Item Category"""
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """ Model string replesantation"""
        return self.category_name

class SubCategory(models.Model):
    """ Model for Item Subcategory"""
    category = models.ForeignKey("ItemCategory", on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        """ Model string replesantation"""
        return self.sub_category


class Report(models.Model):
    """ Model for reported Items"""
    item_id = models.ForeignKey("Item", on_delete=models.CASCADE, null=True, blank=True)
    province = models.CharField(max_length=20, null=True, blank=False)
    district = models.CharField(max_length=20, null=True, blank=True)
    sector = models.CharField(max_length=20, null=True, blank=True)
    report_time = models.DateTimeField()

    def __str__(self) -> str:
        """ Model string representation"""
        return self.item_id.name

