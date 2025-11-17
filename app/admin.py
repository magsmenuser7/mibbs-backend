from django.contrib import admin
from .models import Users, Role, UserRole, Assessment
from simple_history.admin import SimpleHistoryAdmin
import csv, json
from django.http import HttpResponse
from openpyxl import Workbook




@admin.register(Users)
class UsersAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'role', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'role')

@admin.register(Role)
class RoleAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'role_name', 'role_category', 'created_at')
    search_fields = ('role_name',)

@admin.register(UserRole)
class UserRoleAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'user', 'role', 'created_by', 'created_at')
    search_fields = ('user__username', 'role__role_name')




@admin.action(description='Export selected assessments as Excel')
def export_assessments_excel(modeladmin, request, queryset):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Assessments"

    # Excel Header Row
    header = [
        'id', 'username', 'email', 'phone', 'business_name', 'brand_stage',
        'pincode', 'city', 'state', 'industry', 'years_in_business', 
        'digital_maturity', 'primary_goals', 'monthly_revenue', 
        'marketing_spend_band', 'exact_marketing_spend', 'positioning',
        'competitor_notes', 'industry_details', 'created_at'
    ]
    sheet.append(header)

    # Add Data Rows
    for a in queryset:
        sheet.append([
            a.id,
            a.user.username if a.user else '',
            a.user.email if a.user else '',
            a.user.phone if a.user else '',
            a.business_name,
            a.brand_stage,
            a.pincode,
            a.city,
            a.state,
            a.industry,
            a.years_in_business,
            a.digital_maturity,
            json.dumps(a.primary_goals, ensure_ascii=False),
            str(a.monthly_revenue) if a.monthly_revenue is not None else '',
            a.marketing_spend_band,
            str(a.exact_marketing_spend) if a.exact_marketing_spend is not None else '',
            a.positioning,
            a.competitor_notes,
            json.dumps(a.industry_details, ensure_ascii=False) if a.industry_details else '',
            a.created_at.isoformat(),
        ])

    # Return Excel File
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=assessments.xlsx'
    workbook.save(response)
    return response




class AssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'phone',
        'business_name',
        'brand_stage',
        'pincode',
        'city',
        'state',
        'industry',
        'years_in_business',
        'digital_maturity',
        'primary_goals',
        'monthly_revenue',
        'marketing_spend_band',
        'exact_marketing_spend',
        'positioning',
        'competitor_notes',
        'industry_details',
        'created_at',
    )
    
    actions = [export_assessments_excel]   # ✅ replaced CSV with EXCEL









# @admin.action(description='Export selected assessments as CSV')
# def export_assessments_csv(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=assessments.csv'
#     writer = csv.writer(response)

#     # ✅ Include all fields including user fields
#     header = [
#         'id', 'username', 'email', 'phone', 'business_name', 'brand_stage',
#         'pincode', 'city', 'state', 'industry', 'years_in_business', 'digital_maturity',
#         'primary_goals', 'monthly_revenue', 'marketing_spend_band', 'exact_marketing_spend',
#         'positioning', 'competitor_notes', 'industry_details', 'created_at'
#     ]
#     writer.writerow(header)

#     for a in queryset:
#         writer.writerow([
#             a.id,
#             a.user.username if a.user else '',
#             a.user.email if a.user else '',
#             a.user.phone if a.user else '',
#             a.business_name,
#             a.brand_stage,
#             a.pincode,
#             a.city,
#             a.state,
#             a.industry,
#             a.years_in_business,
#             a.digital_maturity,
#             json.dumps(a.primary_goals, ensure_ascii=False),
#             str(a.monthly_revenue) if a.monthly_revenue is not None else '',
#             a.marketing_spend_band,
#             str(a.exact_marketing_spend) if a.exact_marketing_spend is not None else '',
#             a.positioning,
#             a.competitor_notes,
#             json.dumps(a.industry_details, ensure_ascii=False) if a.industry_details else '',
#             a.created_at.isoformat(),
#         ])
#     return response



# class AssessmentAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'username',
#         'email',
#         'phone',
#         'business_name',
#         'brand_stage',
#         'pincode',
#         'city',
#         'state',
#         'industry',
#         'years_in_business',
#         'digital_maturity',
#         'primary_goals',
#         'monthly_revenue',
#         'marketing_spend_band',
#         'exact_marketing_spend',
#         'positioning',
#         'competitor_notes',
#         'industry_details',
#         'created_at',
#     )
#     actions = [export_assessments_csv]

#     # ✅ User fields
#     def username(self, obj):
#         return obj.user.username if obj.user else ''
#     username.short_description = 'User Username'

#     def email(self, obj):
#         return obj.user.email if obj.user else ''
#     email.short_description = 'User Email'

#     def phone(self, obj):
#         return obj.user.phone if obj.user else ''
#     phone.short_description = 'User Phone'

#     # ✅ JSON fields display nicely
#     def primary_goals(self, obj):
#         return json.dumps(obj.primary_goals, ensure_ascii=False)
#     primary_goals.short_description = 'Primary Goals'

#     def industry_details(self, obj):
#         return json.dumps(obj.industry_details, ensure_ascii=False) if obj.industry_details else ''
#     industry_details.short_description = 'Industry Details'





admin.site.register(Assessment, AssessmentAdmin)
# admin.site.register(UserProfile)