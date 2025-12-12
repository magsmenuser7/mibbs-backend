from django.contrib import admin
from .models import Users, Role, UserRole, Assessment,PieChartEntry
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


# class BudgetAllocationInline(admin.TabularInline):
#     model = BudgetAllocation
#     extra = 0


# class BarChartDataInline(admin.TabularInline):
#     model = BarChartData   # FIXED
#     extra = 0

class PieChartEntryInline(admin.TabularInline):
    model = PieChartEntry
    extra = 0




@admin.action(description='Export selected assessments as Excel')
def export_assessments_excel(modeladmin, request, queryset):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Assessment"

    # Excel Header Row
    header = [
        'id', 'username', 'email', 'phone', 'business_name', 'brand_stage',
        'pincode', 'city', 'state', 'industry', 'years_in_business', 
        'digital_maturity', 'primary_goals', 'monthly_revenue', 
        'marketing_spend_band', 'exact_marketing_spend', 'positioning',
        'competitor_notes', 'industry_details','monthly_budget','annual_budget','piechart_str','created_at'
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
            str(a.monthly_budget) if a.monthly_budget is not None else '',
            str(a.annual_budget) if a.annual_budget is not None else '',
            # json.dumps(a.budget_allocations, ensure_ascii=False) if a.budget_allocations else '',
            # json.dumps(a.barchart_data, ensure_ascii=False) if a.barchart_data else '',
            json.dumps([
    {
        "name": item["name"],
        "value": float(item["value"]) if item["value"] is not None else None,
        "amount": float(item["amount"]) if item["amount"] is not None else None,
        "color": item["color"],
    }
    for item in a.pie_chart_entries.all().values('name', 'value', 'amount', 'color')
        ], ensure_ascii=False) if hasattr(a, "pie_chart_entries") else '',
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
        'monthly_budget',
        'annual_budget',
        # 'formatted_bar_chart_data',
        'formatted_pie_chart_entries',
        'created_at',
    )

    actions = [export_assessments_excel]

    inlines = [PieChartEntryInline]



    #  # 👉 Display nested BudgetAllocation items in admin list row
    # def formatted_budget_allocations(self, obj):
    #     allocations = obj.budget_allocation_set.all()  # uses related_name from model
    #     if not allocations:
    #         return "No Data"
    #     return ", ".join([f"{a.channel} ({a.percent}% → ₹{a.amount})" for a in allocations])
    # formatted_budget_allocations.short_description = "Budget Allocation"

    

    # 👉 Display nested ChannelFocus items in admin list row
   # For Bar Chart Data (channel focus)
    # def formatted_bar_chart_data(self, obj):
    #     items = obj.bar_chart_data.all()  # related_name in BarChartData
    #     if not items.exists():
    #         return "No Data"
    #     return ", ".join([f"{i.name} ({i.percentage}% → ₹{i.amount})" for i in items])
    # formatted_bar_chart_data.short_description = "Channel Focus (Bar Chart)"

# For Pie Chart Data
    def formatted_pie_chart_entries(self, obj):
        items = obj.pie_chart_entries.all()  # related_name in PieChartEntry
        if not items.exists():
            return "No Data"
        return ", ".join([f"{i.name} ({i.value}% → ₹{i.amount})" for i in items])
    formatted_pie_chart_entries.short_description = "Pie Chart Entries"

# class BudgetAllocationAdmin(admin.ModelAdmin):
#     list_display = ('assessment', 'channel', 'percent', 'amount')


# class BarChartDataAdmin(admin.ModelAdmin):
#     list_display = ('assessment', 'name', 'percentage', 'amount')


class PieChartEntryAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'name', 'value', 'amount')





# admin.register(BudgetAllocation, BudgetAllocationAdmin)
# admin.register(BarChartData, BarChartDataAdmin)
admin.register(PieChartEntry,PieChartEntryAdmin)
admin.site.register(Assessment, AssessmentAdmin)
# admin.site.register(UserProfile)









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

