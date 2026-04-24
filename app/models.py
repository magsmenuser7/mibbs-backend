from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
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






class NewBusinessQuestionnaire(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)

    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    business_name = models.CharField(max_length=200)
    business_stage = models.CharField(max_length=50)

    has_website = models.BooleanField(default=False)
    website_url = models.URLField(blank=True, null=True)


    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    industry = models.CharField(max_length=100)

    business_type = models.CharField(max_length=50)
    product_business_type = models.CharField(max_length=50, blank=True, null=True)

    starting_budget = models.CharField(max_length=100)

    business_mode = models.JSONField(default=list)
    help_needed = models.JSONField(default=list)

    monthly_budget = models.IntegerField(default=0)
    annual_budget = models.IntegerField(default=0)

    pie_chart_data = models.JSONField(default=list, blank=True)
    channel_focuses = models.JSONField(default=list, blank=True)
    budget_allocations = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
    



class ExistingBusinessQuestionnaire(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)

    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    business_name = models.CharField(max_length=200)
    business_stage = models.CharField(max_length=50)

    has_website = models.BooleanField(default=False)
    website_url = models.URLField(blank=True, null=True)


    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    industry = models.CharField(max_length=100)

    business_type = models.CharField(max_length=50)
    product_business_type = models.CharField(max_length=50, blank=True, null=True)

    years_in_business = models.CharField(max_length=100)

    business_challenges = models.JSONField(default=list)

    digital_scaling_level = models.CharField(max_length=100)

    digital_platforms = models.JSONField(default=list)
    digital_activities = models.JSONField(default=list)

    roi_percentage = models.CharField(max_length=20, blank=True, null=True)

    monthly_revenue = models.CharField(max_length=100)
    marketing_budget_range = models.CharField(max_length=100)

    brand_objectives = models.JSONField(default=list)

    monthly_budget = models.IntegerField(default=0)
    annual_budget = models.IntegerField(default=0)

    pie_chart_data = models.JSONField(default=list, blank=True)
    channel_focuses = models.JSONField(default=list, blank=True)
    budget_allocations = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name







# Employee Onboarding Model

class EmployeeOnboarding(models.Model):

    # STEP 1 — BASIC DETAILS
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    email = models.EmailField()
    mobile = models.CharField(max_length=20)

    doj = models.DateField()
    role = models.CharField(max_length=200)
    division = models.CharField(max_length=200)
    office = models.CharField(max_length=200)

    self_intro = models.TextField()
    linkedin = models.URLField(blank=True,null=True)

    # STEP 2 — PERSONAL DETAILS
    father_name = models.CharField(max_length=200)
    dob = models.DateField()

    address = models.TextField()

    emerg_name = models.CharField(max_length=200)
    emerg_phone = models.CharField(max_length=20)

    blood_group = models.CharField(max_length=10,blank=True,null=True)

    qualification = models.CharField(max_length=200)

    # BANK DETAILS
    acc_name = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    acc_no = models.CharField(max_length=100)
    ifsc = models.CharField(max_length=20)
    branch = models.CharField(max_length=200,blank=True,null=True)

    # REFERENCES
    ref1_name = models.CharField(max_length=200)
    ref1_desg = models.CharField(max_length=200)
    ref1_org = models.CharField(max_length=200)
    ref1_contact = models.CharField(max_length=200)

    ref2_name = models.CharField(max_length=200)
    ref2_desg = models.CharField(max_length=200)
    ref2_org = models.CharField(max_length=200)
    ref2_contact = models.CharField(max_length=200)

    # STEP 3 — DOCUMENTS
    aadhaar_card = models.FileField(upload_to='documents/aadhaar/')
    pan_card = models.FileField(upload_to='documents/pan/')
    photo = models.ImageField(upload_to='documents/photo/')

    tenth_certificate = models.FileField(upload_to='documents/10th/')
    inter_certificate = models.FileField(upload_to='documents/12th/')
    degree_certificate = models.FileField(upload_to='documents/degree/')

    college_id = models.FileField(upload_to='documents/college_id/',blank=True,null=True)
    noc_letter = models.FileField(upload_to='documents/noc/',blank=True,null=True)

    relieving_letter = models.FileField(
        upload_to='documents/relieving/',
        blank=True,
        null=True
    )

    salary_proof = models.FileField(
        upload_to='documents/salary/',
        blank=True,
        null=True
    )

    # STEP 4 & 5
    offer_accepted = models.BooleanField(default=False)
    nda_accepted = models.BooleanField(default=False)

    # STEP 6
    handbook_sections = models.TextField(blank=True)

    # STEP 7
    signature = models.CharField(max_length=200)
    sign_date = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"







class EODReport(models.Model):

    # ========================
    # EMPLOYEE DETAILS
    # ========================
    employee_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    # ========================
    # DATE DETAILS
    # ========================
    date = models.CharField(max_length=100)
    date_iso = models.DateField()
    weekday = models.CharField(max_length=50)

    # ========================
    # TIME DETAILS
    # ========================
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.CharField(max_length=50)

    # ========================
    # TASK SUMMARY
    # ========================
    tasks_count = models.IntegerField()
    min_tasks = models.IntegerField()
    met_minimum = models.CharField(max_length=10)

    tasks_done = models.IntegerField()
    tasks_partial = models.IntegerField()
    tasks_carried = models.IntegerField()
    tasks_blocked = models.IntegerField()

    # ========================
    # TASK DETAILS
    # ========================
    tasks_text = models.TextField()
    tasks_json = models.JSONField()

    # ========================
    # MEETINGS
    # ========================
    no_meetings = models.CharField(max_length=10)
    meetings_count = models.IntegerField()
    meetings_text = models.TextField()
    meetings_json = models.JSONField()

    # ========================
    # OUTPUT / DELIVERABLES
    # ========================
    deliverables = models.TextField()

    # ========================
    # BLOCKERS
    # ========================
    has_blocker = models.CharField(max_length=10)
    blocker_text = models.TextField(blank=True, null=True)

    # ========================
    # TOMORROW PLAN
    # ========================
    tomorrow_plan = models.TextField(blank=True, null=True)

    # ========================
    # MOOD
    # ========================
    mood_score = models.IntegerField()
    mood_label = models.CharField(max_length=50)
    mood_emoji = models.CharField(max_length=10)

    # ========================
    # NOTES
    # ========================
    general_note = models.TextField(blank=True, null=True)

    # ========================
    # SUBMISSION INFO
    # ========================
    submitted_at = models.CharField(max_length=100)
    hr_email = models.EmailField()

    # ========================
    # AUTO FIELDS
    # ========================
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} - {self.date_iso}"