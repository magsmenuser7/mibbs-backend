from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords
from django.conf import settings



# Create your models here.


# User Manager
class UserManager(BaseUserManager):
    # use_in_migrations = True
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not phone:
            raise ValueError("Phone number is required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None):
        user = self.create_user(email, username, phone, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Role Model
class Role(models.Model):
    ROLE_CATEGORIES = [
        ("admin", "Admin"),
        ("dealer", "Dealer"),
        ("customer", "Customer"),
    ]
    
    role_name = models.CharField(max_length=100, unique=True)
    role_category = models.CharField(max_length=100, choices=ROLE_CATEGORIES, default="customer")
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def _str_(self):
        return self.role_name

    class Meta:
        db_table = 'role'




#  User Model with Role
class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    username = models.CharField(max_length=100, unique=True, blank=False, null=False)
    profile_image = models.TextField(blank=True, null=True)
    firebase_id = models.TextField(blank=True, null=True, default=None)
    date_of_birth = models.DateField(blank=True, null=True, default=None)
    pincode = models.IntegerField(blank=True, null=True, default=None)
    address = models.TextField(blank=True, null=True, default=None)
    otp = models.IntegerField(blank=True, null=True,default=None)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone"]

    objects = UserManager()
    history = HistoricalRecords()

    def _str_(self):
        return self.username

    class Meta:
        db_table = 'users'


# User Role Assignment Model (Many-to-Many)
class UserRole(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_users")
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="created_roles")
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def _str_(self):
        return f"{self.user.username} - {self.role.role_name}"

    class Meta:
        db_table = 'user_role'
        unique_together = ("user", "role")






# class UserProfile(models.Model):
#   user = models.OneToOneField(settings.AUTH_USER_MODEL,unique=True,on_delete=models.CASCADE,related_name='profile')
#   phone = models.CharField(max_length=20, blank=True)
#   created_at = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#     return f"{self.user.email} profile"
  







class Assessment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)

    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    business_name = models.CharField(max_length=255, blank=True)
    brand_stage = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    industry = models.CharField(max_length=128, blank=True)
    years_in_business = models.IntegerField(null=True, blank=True)
    digital_maturity = models.CharField(max_length=100, blank=True)

    primary_goals = models.JSONField(default=list, blank=True)
    monthly_revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    marketing_spend_band = models.CharField(max_length=50, blank=True)
    exact_marketing_spend = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    positioning = models.CharField(max_length=100, blank=True)
    competitor_notes = models.TextField(blank=True)

    industry_details = models.JSONField(null=True, blank=True)
    monthly_budget = models.FloatField(default=0, null=True, blank=True)
    annual_budget = models.FloatField(default=0, null=True, blank=True)

    # budget_allocations = models.JSONField(default=list, blank=True)
    # barchart_data = models.TextField(default=list, blank=True)
    piechart_str = models.TextField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# class BudgetAllocation(models.Model):
#     assessment = models.ForeignKey(
#         Assessment,
#         on_delete=models.CASCADE,
#         related_name="budget_allocation_set"
#     )
#     channel = models.CharField(max_length=100)
#     percent = models.FloatField(null=True, blank=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)


# class BarChartData(models.Model):
#     assessment = models.ForeignKey(
#         Assessment,
#         on_delete=models.CASCADE,
#         related_name="bar_chart_data"
#     )
#     name = models.CharField(max_length=100)
#     percentage = models.FloatField(null=True, blank=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)




class PieChartEntry(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="pie_chart_entries"
    )
    name = models.CharField(max_length=100)
    value = models.FloatField(null=True, blank=True)  # % value
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    color = models.CharField(max_length=20, blank=True, null=True)