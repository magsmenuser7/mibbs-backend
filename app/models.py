from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords
from django.conf import settings
import secrets
from datetime import timedelta
from django.utils import timezone



# Create your models here.


# User Manager
class UserManager(BaseUserManager):# User Manager
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

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'role'




# User Model with Role
class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    username = models.CharField(max_length=100, blank=False, null=False)
    profile_image = models.TextField(blank=True, null=True)
    firebase_id = models.TextField(blank=True, null=True, default=None)
    date_of_birth = models.DateField(blank=True, null=True, default=None)
    pincode = models.IntegerField(blank=True, null=True, default=None)
    address = models.TextField(blank=True, null=True, default=None)
    otp = models.IntegerField(blank=True, null=True, default=None)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    
    # ✅ NEW: Password Reset Fields
    reset_token = models.CharField(max_length=6, blank=True, null=True)
    reset_token_created_at = models.DateTimeField(blank=True, null=True)

    # ✅ Login with OTP (NEW)
    login_otp = models.CharField(max_length=6, blank=True, null=True)
    login_otp_created_at = models.DateTimeField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone"]

    objects = UserManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

    # ✅ NEW: Password Reset Methods
    def generate_reset_token(self):
        """Generate a unique 6-digit reset token"""
        self.reset_token = str(secrets.randbelow(900000) + 100000)  # 6-digit token
        self.reset_token_created_at = timezone.now()
        self.save()
        return self.reset_token

    def is_reset_token_valid(self):
        """Check if reset token is still valid (24 hours)"""
        if not self.reset_token or not self.reset_token_created_at:
            return False
        
        expiry_time = self.reset_token_created_at + timedelta(hours=24)
        return timezone.now() < expiry_time

    def clear_reset_token(self):
        """Clear reset token after use"""
        self.reset_token = None
        self.reset_token_created_at = None
        self.save()



    # ✅ ADD THESE METHODS HERE (INSIDE CLASS)
    def generate_login_otp(self):
        self.login_otp = str(secrets.randbelow(900000) + 100000)
        self.login_otp_created_at = timezone.now()
        self.save()
        return self.login_otp

    def is_login_otp_valid(self):
        if not self.login_otp or not self.login_otp_created_at:
            return False

        expiry_time = self.login_otp_created_at + timedelta(minutes=10)
        return timezone.now() < expiry_time

    def clear_login_otp(self):
        self.login_otp = None
        self.login_otp_created_at = None
        self.save()



# User Role Assignment Model (Many-to-Many)
class UserRole(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_users")
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name="created_roles")
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"

    class Meta:
        db_table = 'user_role'
        unique_together = ("user", "role")




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
    months_in_business = models.IntegerField(null=True, blank=True)
    digital_maturity = models.CharField(max_length=100, blank=True)

    primary_goals = models.JSONField(default=list, blank=True)
    monthly_revenue = models.IntegerField(null=True, blank=True)
    marketing_spend_band = models.CharField(max_length=50, blank=True)
    exact_marketing_spend = models.IntegerField(null=True, blank=True)
    positioning = models.CharField(max_length=100, blank=True)
    competitor_notes = models.TextField(blank=True)
    industry_details = models.JSONField(null=True, blank=True)
    monthly_budget = models.IntegerField(default=0, null=True, blank=True)
    annual_budget = models.IntegerField(default=0, null=True, blank=True)
    piechart_str = models.CharField(max_length=5000, default=list, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # budget_allocations = models.JSONField(default=list, blank=True)
    # barchart_data = models.TextField(default=list, blank=True)
    # exact_marketing_spend = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)


    # def __str__(self):
    #     return f"Assessment by {self.user.username if self.user else 'Guest'} - {self.business_name}"



class PieChartEntry(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="pie_chart_entries"
    )
    name = models.CharField(max_length=100)
    value = models.FloatField(null=True, blank=True)  # % value
    amount = models.IntegerField(default=0, null=True, blank=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.value}%"





class Intaklksstatspupdate(models.Model):
    youtubestats = models.CharField(max_length=255, blank=True, null=True)
    instagramstats = models.CharField(max_length=255, blank=True, null=True)
    communitygrowthstats = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='intaklks_stats/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    guestname = models.CharField(max_length=255, blank=True, null=True)
    podcasttime = models.CharField(max_length=50, blank=True, null=True)
    podcastdate = models.DateField(blank=True, null=True)
    podcastnumber = models.IntegerField(blank=True, null=True)
    youtubelink = models.URLField(max_length=500, blank=True, null=True)
    podcastviews = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.youtubestats or "No YouTube Stats"


