from rest_framework import serializers
from .models import Users, Role, UserRole, Assessment,PieChartEntry
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

Users = get_user_model() 



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True, required=False
    )

    class Meta:
        model = Users
        exclude = ('password',)  # ✅ Removed 'history'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'email', 'phone', 'password')

    def validate(self, data):
        if Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        if Users.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        if Users.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError({'phone': 'Phone number already exists'})
        return data

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user
    


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # this can be email or phone
    password = serializers.CharField(write_only=True)



# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     phone = serializers.CharField(required=False, allow_blank=True)
#     password = serializers.CharField(write_only=True)











class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, allow_blank=True, required=False)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Users
        fields = ['username', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        data['password'] = make_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = Users.objects.create(**validated_data)
        return user
    



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



# class BudgetAllocationSerializer(serializers.Serializer):
#     channel = serializers.CharField()
#     percent = serializers.FloatField(required=False)
#     amount = serializers.FloatField(required=False)

# class BarChartDataSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     percentage = serializers.FloatField()
#     amount = serializers.FloatField(required=False)

class PieChartEntrySerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.FloatField()       # Percentage value
    amount = serializers.FloatField()      # Budget amount
    color = serializers.CharField(required=False, allow_blank=True)

class AssessmentSerializer(serializers.ModelSerializer):
    # User info (read-only)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    # Map frontend camelCase keys
    businessName = serializers.CharField(source='business_name', required=False, allow_blank=True)
    brandStage = serializers.CharField(source='brand_stage', required=False, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)
    yearsInBusiness = serializers.IntegerField(source='years_in_business', required=False, allow_null=True)
    digitalMaturity = serializers.CharField(source='digital_maturity', required=False, allow_blank=True)
    primaryGoals = serializers.JSONField(source='primary_goals', required=False, allow_null=True)
    monthlyRevenue = serializers.DecimalField(source='monthly_revenue', max_digits=20, decimal_places=2, required=False, allow_null=True)
    marketingSpendBand = serializers.CharField(source='marketing_spend_band', required=False, allow_blank=True)
    exactMarketingSpend = serializers.DecimalField(source='exact_marketing_spend', max_digits=20, decimal_places=2, required=False, allow_null=True)
    positioning = serializers.CharField(required=False, allow_blank=True)
    competitorNotes = serializers.CharField(source='competitor_notes', required=False, allow_blank=True)
    industryDetails = serializers.JSONField(source='industry_details', required=False, allow_null=True)
    
    monthlyBudget = serializers.FloatField(source='monthly_budget', required=False)
    annualBudget = serializers.FloatField(source='annual_budget', required=False)

    # Nested relational fields
    # budgetAllocations = BudgetAllocationSerializer(many=True, required=False)
    # barchartdata = BarChartDataSerializer(many=True, required=False)
    pieChartData = PieChartEntrySerializer(many=True, required=False)  # Added for pie chart

    class Meta:
        model = Assessment
        fields = [
            'id', 'username', 'email', 'phone',
            'businessName', 'brandStage', 'pincode', 'city', 'state', 'industry',
            'yearsInBusiness', 'digitalMaturity', 'primaryGoals',
            'monthlyRevenue', 'marketingSpendBand', 'exactMarketingSpend',
            'positioning', 'competitorNotes', 'industryDetails',
            'monthlyBudget', 'annualBudget', 'pieChartData',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'username', 'email', 'phone']

    def validate_primary_goals(self, value):
        """Allow up to 4 primary goals"""
        if isinstance(value, list) and len(value) > 4:
            raise serializers.ValidationError("You can select up to 4 primary goals.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = None

        # Extract nested fields
        # budget_allocations_data = validated_data.pop('budgetAllocations', [])
        # bar_chart_data = validated_data.pop('barchartdata', [])
        piechart_data = validated_data.pop('pieChartData', [])

        # Attach user if available
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        else:
            email = self.context.get('request').data.get('email')
            if email:
                user = Users.objects.filter(email=email).first()

        if user:
            validated_data['user'] = user
            validated_data['username'] = user.username
            validated_data['email'] = user.email
            validated_data['phone'] = getattr(user, 'phone', '')

        # Create Assessment
        assessment = Assessment.objects.create(**validated_data)

        # # Nested BudgetAllocations
        # for ba in budget_allocations_data:
        #     BudgetAllocation.objects.create(assessment=assessment, **ba)

        # Nested ChannelFocuses
        # for cf in bar_chart_data:
        #     BarChartData.objects.create(assessment=assessment, **cf)

        # Nested PieChartEntries
        for pc in piechart_data:
            PieChartEntry.objects.create(assessment=assessment, **pc)

        return assessment


# class AssessmentSerializer(serializers.ModelSerializer):
#     # Include user info (read-only)
#     username = serializers.CharField(source='user.username', read_only=True)
#     email = serializers.EmailField(source='user.email', read_only=True)
#     phone = serializers.CharField(source='user.phone', read_only=True)

#     # Map frontend camelCase keys to backend model fields
#     businessName = serializers.CharField(source='business_name', required=False, allow_blank=True)
#     brandStage = serializers.CharField(source='brand_stage', required=False, allow_blank=True)
#     pincode = serializers.CharField(required=False, allow_blank=True)
#     city = serializers.CharField(required=False, allow_blank=True)
#     state = serializers.CharField(required=False, allow_blank=True)
#     industry = serializers.CharField(required=False, allow_blank=True)
#     yearsInBusiness = serializers.IntegerField(source='years_in_business', required=False, allow_null=True)
#     digitalMaturity = serializers.CharField(source='digital_maturity', required=False, allow_blank=True)
#     primaryGoals = serializers.JSONField(source='primary_goals', required=False, allow_null=True)
#     monthlyRevenue = serializers.DecimalField(source='monthly_revenue', max_digits=20, decimal_places=2, required=False, allow_null=True)
#     marketingSpendBand = serializers.CharField(source='marketing_spend_band', required=False, allow_blank=True)
#     exactMarketingSpend = serializers.DecimalField(source='exact_marketing_spend', max_digits=20, decimal_places=2, required=False, allow_null=True)
#     positioning = serializers.CharField(required=False, allow_blank=True)
#     competitorNotes = serializers.CharField(source='competitor_notes', required=False, allow_blank=True)
#     industryDetails = serializers.JSONField(source='industry_details', required=False, allow_null=True)
#     monthlyBudget = serializers.DecimalField(source='monthly_budget', max_digits=12, decimal_places=2, required=False, allow_null=True)
#     annualBudget = serializers.DecimalField(source='annual_budget', max_digits=12, decimal_places=2, required=False, allow_null=True)
#     budgetAllocations = serializers.JSONField(source='budget_allocations', required=False, allow_null=True)
#     channelFocuses = serializers.JSONField(source='channel_focuses', required=False, allow_null=True)

#     class Meta:
#         model = Assessment
#         fields = [
#             'id',
#             'username', 'email', 'phone',  # linked user info
#             'businessName', 'brandStage', 'pincode', 'city', 'state', 'industry',
#             'yearsInBusiness', 'digitalMaturity', 'primaryGoals',
#             'monthlyRevenue', 'marketingSpendBand', 'exactMarketingSpend',
#             'positioning', 'competitorNotes', 'industryDetails','monthlyBudget','annualBudget','budgetAllocations','channelFocuses',
#             'created_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'username', 'email', 'phone']

#     def validate_primary_goals(self, value):
#         """Allow up to 4 primary goals"""
#         if isinstance(value, list) and len(value) > 4:
#             raise serializers.ValidationError("You can select up to 4 primary goals.")
#         return value

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = None

#         if request and hasattr(request, 'user') and request.user.is_authenticated:
#             user = request.user
#         else:
#             email = request.data.get('email')
#         if email:
#             user = Users.objects.filter(email=email).first()

#     # Set user-related fields in assessment table
#         if user:
#             validated_data['user'] = user
#             validated_data['username'] = user.username
#             validated_data['email'] = user.email
#             validated_data['phone'] = getattr(user, 'phone', '')

#         assessment = Assessment.objects.create(**validated_data)
#         return assessment
