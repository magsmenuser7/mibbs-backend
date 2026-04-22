from django.contrib import admin
from .models import Users, Role, UserRole, Assessment,PieChartEntry,Intaklksstatspupdate,NewBusinessQuestionnaire,ExistingBusinessQuestionnaire,EmployeeOnboarding
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
        'pincode', 'city', 'state', 'industry', 'years_in_business','months_in_business', 
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
            a.months_in_business,
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
        'months_in_business',
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
        'formatted_pie_chart_entries',
        'created_at',
    )

    actions = [export_assessments_excel]

    inlines = [PieChartEntryInline]






# For Pie Chart Data
    def formatted_pie_chart_entries(self, obj):
        items = obj.pie_chart_entries.all()  # related_name in PieChartEntry
        if not items.exists():
            return "No Data"
        return ", ".join([f"{i.name} ({i.value}% → ₹{i.amount})" for i in items])
    formatted_pie_chart_entries.short_description = "Pie Chart Entries"




class PieChartEntryAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'name', 'value', 'amount')



class IntaklksstatspupdateAdmin(admin.ModelAdmin):
    list_display = ('youtubestats', 'instagramstats', 'communitygrowthstats','image', 'title', 'description','podcasttime', 'podcastdate', 'podcastnumber', 'guestname', 'youtubelink','podcastviews', 'last_updated')



from django.contrib import admin
from .models import NewBusinessQuestionnaire, ExistingBusinessQuestionnaire


# ================================
# NEW BUSINESS ADMIN
# ================================


class NewBusinessQuestionnaireAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "business_name",
        "industry",
        "business_type",
        "starting_budget",
        "monthly_budget",
        "annual_budget",
        "created_at"
    )

    search_fields = (
        "username",
        "email",
        "phone",
        "business_name",
        "industry",
    )

    list_filter = (
        "industry",
        "business_type",
        "created_at",
    )

    readonly_fields = (
        "monthly_budget",
        "annual_budget",
        "pie_chart_data",
        "channel_focuses",
        "budget_allocations",
        "created_at",
    )

    fieldsets = (

        ("User Information", {
            "fields": (
                "user",
                "username",
                "email",
                "phone",
            )
        }),

        ("Business Information", {
            "fields": (
                "business_name",
                "business_stage",
                "industry",
                "business_type",
                "product_business_type",
            )
        }),

        ("Website Information", {
            "fields": (
                "has_website",
                "website_url",
            )
        }),

        ("Location Details", {
            "fields": (
                "pincode",
                "locality",
                "district",
                "state",
                "country",
            )
        }),

        ("New Business Details", {
            "fields": (
                "starting_budget",
                "business_mode",
                "help_needed",
            )
        }),

        ("Budget Report", {
            "fields": (
                "monthly_budget",
                "annual_budget",
                "pie_chart_data",
                "channel_focuses",
                "budget_allocations",
            )
        }),

        ("System Info", {
            "fields": (
                "created_at",
            )
        }),
    )


# ================================
# EXISTING BUSINESS ADMIN
# ================================


class ExistingBusinessQuestionnaireAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "business_name",
        "industry",
        "years_in_business",
        "monthly_revenue",
        "marketing_budget_range",
        "monthly_budget",
        "annual_budget",
        "created_at"
    )

    search_fields = (
        "username",
        "email",
        "phone",
        "business_name",
        "industry",
    )

    list_filter = (
        "industry",
        "digital_scaling_level",
        "created_at",
    )

    readonly_fields = (
        "monthly_budget",
        "annual_budget",
        "pie_chart_data",
        "channel_focuses",
        "budget_allocations",
        "created_at",
    )

    fieldsets = (

        ("User Information", {
            "fields": (
                "user",
                "username",
                "email",
                "phone",
            )
        }),

        ("Business Information", {
            "fields": (
                "business_name",
                "business_stage",
                "industry",
                "business_type",
                "product_business_type",
            )
        }),

        ("Website Information", {
            "fields": (
                "has_website",
                "website_url",
            )
        }),

        ("Location Details", {
            "fields": (
                "pincode",
                "locality",
                "district",
                "state",
                "country",
            )
        }),

        ("Experience", {
            "fields": (
                "years_in_business",
                "business_challenges",
            )
        }),

        ("Digital Presence", {
            "fields": (
                "digital_scaling_level",
                "digital_platforms",
                "digital_activities",
                "roi_percentage",
            )
        }),

        ("Revenue & Marketing", {
            "fields": (
                "monthly_revenue",
                "marketing_budget_range",
                "brand_objectives",
            )
        }),

        ("Budget Report", {
            "fields": (
                "monthly_budget",
                "annual_budget",
                "pie_chart_data",
                "channel_focuses",
                "budget_allocations",
            )
        }),

        ("System Info", {
            "fields": (
                "created_at",
            )
        }),
    )




class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "email",
        "mobile",
        "role",
        "division",
        "office",
        "created_at"
    )







admin.register(PieChartEntry,PieChartEntryAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Intaklksstatspupdate, IntaklksstatspupdateAdmin)
admin.site.register(NewBusinessQuestionnaire)
admin.site.register(ExistingBusinessQuestionnaire)
admin.site.register(EmployeeOnboarding,EmployeeAdmin)






