
# views.py
from email.quoprimime import header_check

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from django.contrib.auth import login as django_login
from urllib3 import request
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,AssessmentSerializer,Intaklksstatspupdate,IntalksStatsSerializer,NewBusinessSerializer, ExistingBusinessSerializer,EODReportSerializer
from .models import Intaklksstatspupdate, Users, EmployeeOnboarding,EODReport
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from .brevo_utility import send_to_brevo,send_password_reset_email
from dotenv import load_dotenv
from .serializers import ForgotPasswordSerializer,VerifyOtpSerializer,ResetPasswordSerializer,LoginOtpSendSerializer,LoginOtpVerifySerializer
from django.utils import timezone  # <--- Added this
from datetime import timedelta     # <--- Required for expiry logic
from django.db.models import Max
from rest_framework.decorators import api_view
import requests
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def submit_onboarding(request):

    if request.method == "POST":

        employee = EmployeeOnboarding.objects.create(

            first_name=request.POST.get("firstName"),
            last_name=request.POST.get("lastName"),

            email=request.POST.get("email"),
            mobile=request.POST.get("mobile"),

            doj=request.POST.get("doj"),
            role=request.POST.get("role"),
            division=request.POST.get("division"),
            office=request.POST.get("office"),

            self_intro=request.POST.get("selfIntro"),
            linkedin=request.POST.get("linkedin"),

            father_name=request.POST.get("fatherName"),
            dob=request.POST.get("dob"),
            address=request.POST.get("address"),

            emerg_name=request.POST.get("emergName"),
            emerg_phone=request.POST.get("emergPhone"),

            blood_group=request.POST.get("bloodGroup"),
            qualification=request.POST.get("qual"),

            acc_name=request.POST.get("accName"),
            bank_name=request.POST.get("bankName"),
            acc_no=request.POST.get("accNo"),
            ifsc=request.POST.get("ifsc"),
            branch=request.POST.get("branch"),

            ref1_name=request.POST.get("ref1Name"),
            ref1_desg=request.POST.get("ref1Desg"),
            ref1_org=request.POST.get("ref1Org"),
            ref1_contact=request.POST.get("ref1Contact"),

            ref2_name=request.POST.get("ref2Name"),
            ref2_desg=request.POST.get("ref2Desg"),
            ref2_org=request.POST.get("ref2Org"),
            ref2_contact=request.POST.get("ref2Contact"),

            aadhaar_card=request.FILES.get("aadhaar"),
            pan_card=request.FILES.get("pan"),
            photo=request.FILES.get("photo"),

            tenth_certificate=request.FILES.get("tenth"),
            inter_certificate=request.FILES.get("twelfth"),
            degree_certificate=request.FILES.get("degree"),

            college_id=request.FILES.get("collegeid"),
            noc_letter=request.FILES.get("noc"),
            relieving_letter=request.FILES.get("relieving"),
            salary_proof=request.FILES.get("salary"),

            offer_accepted=request.POST.get("offerCb") == "true",
            nda_accepted=request.POST.get("ndaCb") == "true",

            handbook_sections=request.POST.get("hb_sections"),

            signature=request.POST.get("signature"),
            sign_date=request.POST.get("signDate"),
        )

        # Document URLs
        aadhaar = request.build_absolute_uri(employee.aadhaar_card.url) if employee.aadhaar_card else ""
        pan = request.build_absolute_uri(employee.pan_card.url) if employee.pan_card else ""
        photo = request.build_absolute_uri(employee.photo.url) if employee.photo else ""
        tenth = request.build_absolute_uri(employee.tenth_certificate.url) if employee.tenth_certificate else ""
        inter = request.build_absolute_uri(employee.inter_certificate.url) if employee.inter_certificate else ""
        degree = request.build_absolute_uri(employee.degree_certificate.url) if employee.degree_certificate else ""
        college = request.build_absolute_uri(employee.college_id.url) if employee.college_id else ""
        noc = request.build_absolute_uri(employee.noc_letter.url) if employee.noc_letter else ""
       
        relieving_url = request.build_absolute_uri(employee.relieving_letter.url) if employee.relieving_letter else ""
        salary_url = request.build_absolute_uri(employee.salary_proof.url) if employee.salary_proof else ""


        subject = "New Employee Onboarding Submission"

        # Helper style for section headers
        header_style = "background-color: #f2f2f2; font-weight: bold; padding: 10px; border: 1px solid #ddd; color: #333;"
        cell_style = "padding: 8px; border: 1px solid #ddd; vertical-align: top;"
        label_style = "font-weight: bold; width: 30%; background-color: #fafafa; " + cell_style

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: auto; border: 1px solid #eee; padding: 20px;">
            <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">New Employee Onboarding Submission</h2>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr><td colspan="2" style="{header_style}">Basic Details</td></tr>
                <tr><td style="{label_style}">Name</td><td style="{cell_style}">{employee.first_name} {employee.last_name}</td></tr>
                <tr><td style="{label_style}">Email</td><td style="{cell_style}">{employee.email}</td></tr>
                <tr><td style="{label_style}">Mobile</td><td style="{cell_style}">{employee.mobile}</td></tr>
                <tr><td style="{label_style}">Role</td><td style="{cell_style}">{employee.role}</td></tr>
                <tr><td style="{label_style}">Division</td><td style="{cell_style}">{employee.division}</td></tr>
                <tr><td style="{label_style}">Office</td><td style="{cell_style}">{employee.office}</td></tr>
                <tr><td style="{label_style}">Date of Joining</td><td style="{cell_style}">{employee.doj}</td></tr>

                <tr><td colspan="2" style="{header_style}">Personal Details</td></tr>
                <tr><td style="{label_style}">Father's Name</td><td style="{cell_style}">{employee.father_name}</td></tr>
                <tr><td style="{label_style}">Date of Birth</td><td style="{cell_style}">{employee.dob}</td></tr>
                <tr><td style="{label_style}">Address</td><td style="{cell_style}">{employee.address}</td></tr>
                <tr><td style="{label_style}">Emergency Contact</td><td style="{cell_style}">{employee.emerg_name} - {employee.emerg_phone}</td></tr>
                <tr><td style="{label_style}">Blood Group</td><td style="{cell_style}">{employee.blood_group}</td></tr>

                <tr><td colspan="2" style="{header_style}">Bank Details</td></tr>
                <tr><td style="{label_style}">Account Name</td><td style="{cell_style}">{employee.acc_name}</td></tr>
                <tr><td style="{label_style}">Bank Name</td><td style="{cell_style}">{employee.bank_name}</td></tr>
                <tr><td style="{label_style}">Account Number</td><td style="{cell_style}">{employee.acc_no}</td></tr>
                <tr><td style="{label_style}">IFSC</td><td style="{cell_style}">{employee.ifsc}</td></tr>

                <tr><td colspan="2" style="{header_style}">Professional References</td></tr>
                <tr><td style="{label_style}">Reference 1</td><td style="{cell_style}">{employee.ref1_name} ({employee.ref1_desg})<br>{employee.ref1_org} - {employee.ref1_contact}</td></tr>
                <tr><td style="{label_style}">Reference 2</td><td style="{cell_style}">{employee.ref2_name} ({employee.ref2_desg})<br>{employee.ref2_org} - {employee.ref2_contact}</td></tr>

                <tr><td colspan="2" style="{header_style}">Documents</td></tr>
                <tr>
                    <td colspan="2" style="{cell_style}">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            {doc_link("Aadhaar Card", aadhaar)} | {doc_link("PAN Card", pan)} | {doc_link("Photo", photo)}<br>
                            {doc_link("10th Certificate", tenth)} | {doc_link("12th Certificate", inter)} | {doc_link("Degree Certificate", degree)}<br>
                            {doc_link("College ID", college)} | {doc_link("NOC Letter", noc)}<br>
                            {doc_link("Relieving Letter", relieving_url)} | {doc_link("Salary Proof", salary_url)}
                        </div>
                    </td>
                </tr>

                <tr><td colspan="2" style="{header_style}">Declaration</td></tr>
                <tr><td style="{label_style}">Offer Accepted</td><td style="{cell_style}">{employee.offer_accepted}</td></tr>
                <tr><td style="{label_style}">NDA Accepted</td><td style="{cell_style}">{employee.nda_accepted}</td></tr>
                <tr><td style="{label_style}">Signature</td><td style="{cell_style}">{employee.signature}</td></tr>
                <tr><td style="{label_style}">Sign Date</td><td style="{cell_style}">{employee.sign_date}</td></tr>
            </table>

            <p style="font-size: 12px; color: #7f8c8d;">Submitted at: {employee.created_at}</p>
        </div>
        """ 

        # subject = "New Employee Onboarding Submission"

        # html_content = f"""

        # <h3>Basic Details</h3>
        # <p><b>Name:</b> {employee.first_name} {employee.last_name}</p>
        # <p><b>Email:</b> {employee.email}</p>
        # <p><b>Mobile:</b> {employee.mobile}</p>
        # <p><b>Role:</b> {employee.role}</p>
        # <p><b>Division:</b> {employee.division}</p>
        # <p><b>Office:</b> {employee.office}</p>
        # <p><b>Date of Joining:</b> {employee.doj}</p>

        # <h3>Personal Details</h3>
        # <p><b>Father Name:</b> {employee.father_name}</p>
        # <p><b>Date of Birth:</b> {employee.dob}</p>
        # <p><b>Address:</b> {employee.address}</p>
        # <p><b>Emergency Contact:</b> {employee.emerg_name} - {employee.emerg_phone}</p>
        # <p><b>Blood Group:</b> {employee.blood_group}</p>

        # <h3>Bank Details</h3>
        # <p><b>Account Name:</b> {employee.acc_name}</p>
        # <p><b>Bank Name:</b> {employee.bank_name}</p>
        # <p><b>Account Number:</b> {employee.acc_no}</p>
        # <p><b>IFSC:</b> {employee.ifsc}</p>

        # <h3>Professional References</h3>
        # <p><b>Reference 1:</b> {employee.ref1_name} ({employee.ref1_desg})</p>
        # <p>{employee.ref1_org} - {employee.ref1_contact}</p>

        # <p><b>Reference 2:</b> {employee.ref2_name} ({employee.ref2_desg})</p>
        # <p>{employee.ref2_org} - {employee.ref2_contact}</p>

        # <h3>Documents</h3>

        # {doc_link("Aadhaar Card", aadhaar)}
        # {doc_link("PAN Card", pan)}
        # {doc_link("Photo", photo)}

        # {doc_link("10th Certificate", tenth)}
        # {doc_link("12th Certificate", inter)}
        # {doc_link("Degree Certificate", degree)}

        # {doc_link("College ID", college)}
        # {doc_link("NOC Letter", noc)}

        # {doc_link("Relieving Letter", relieving_url)}
        # {doc_link("Salary Proof", salary_url)}

        # <h3>Declaration</h3>
        # <p><b>Offer Letter Accepted:</b> {employee.offer_accepted}</p>
        # <p><b>NDA Accepted:</b> {employee.nda_accepted}</p>
        # <p><b>Signature:</b> {employee.signature}</p>
        # <p><b>Sign Date:</b> {employee.sign_date}</p>

        # <hr>
        # <p>Submitted at: {employee.created_at}</p>
        # """

        email = EmailMultiAlternatives(
            subject,
            "",
            settings.EMAIL_HOST_USER,
            [
                "hr@magsmen.com",
                "ceo@grofession.com",
                # "ajaychimata205@gmail.com",
                # "kajasuresh522@gmail.com",
                # employee.email
            ]
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        # return JsonResponse({
        #     "status": "success",
        #     "message": "Onboarding submitted and email sent successfully"
        # })

    employee_message = f"""
        Dear {employee.first_name},

        We are pleased to inform you that you have successfully completed the digital onboarding process. On behalf of the entire team at Magsmen, we warmly welcome you aboard.

        Please find below an outline of your structured integration plan for the coming weeks:

        1. Day 1–3 | Reading Period  
        Full handbook review. You will not be assigned client work during this phase.

        2. Day 3–7 | Shadowing Period  
        You will be paired with a senior team member to observe day-to-day operations and team workflows.

        3. Week 2–4 | Supervised Work  
        You will undertake assigned tasks under supervision, with daily written feedback provided to support your development.

        4. Day 30 | First Performance Check-In  
        A formal review meeting with the Head of Operations to assess your initial progress and address any concerns.

        5. Day 90 | Probation Review  
        A comprehensive formal assessment measured against the success criteria defined for your role.

        We are confident that this structured approach will help you transition smoothly into your new role. Please ensure you familiarise yourself with the onboarding materials and do not hesitate to seek guidance as needed.

        For any queries, please contact the HR team:
        hr@magsmen.com
        +91 90449 10449

        Best Regards,  
        Magsmen Team
        """

    send_mail(
        "Welcome to Magsmen 🚀",
        employee_message,
        settings.EMAIL_HOST_USER,
         [employee.email],
            fail_silently=False
        )

        # =========================
        # END NEW CODE
        # =========================


    return JsonResponse({
        "status": "success",
        "message": "Onboarding submitted and email sent successfully"
    })



def doc_link(label, url):
    if url:
        return f'<p>{label}: <a href="{url}" target="_blank">VIEW</a></p>'
    return f'<p>{label}: Not Uploaded</p>'




# Grofesion daily work report - EOD Report

@api_view(['POST'])
def submit_eod(request):
    serializer = EODReportSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()

        subject = f"EOD Report - {instance.employee_name} ({instance.date_iso})"

        # Plain Text Fallback
        message = f"EOD REPORT\n\nEmployee: {instance.employee_name}\nDate: {instance.date}\nTotal Hours: {instance.total_hours}"

        # CSS Styles for Email Clients
        table_style = "width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; margin-bottom: 20px; border: 1px solid #e0e0e0;"
        header_style = "background-color: #E8510A; color: white; padding: 12px; text-align: left; font-size: 16px; border: 1px solid #E8510A;"
        label_style = "background-color: #f9f9f9; font-weight: bold; padding: 10px; border: 1px solid #e0e0e0; width: 30%; color: #333;"
        value_style = "padding: 10px; border: 1px solid #e0e0e0; color: #555;"
        sub_header = "background-color: #f2f2f2; font-weight: bold; padding: 10px; border: 1px solid #e0e0e0; color: #E8510A; text-transform: uppercase; font-size: 13px;"

        # HTML Content
        html_content = f"""
        <div style="background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 700px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #ddd;">
                <h2 style="color: #E8510A; margin-top: 0; border-bottom: 2px solid #E8510A; padding-bottom: 10px;">Daily End of Day (EOD) Report</h2>
                
                <table style="{table_style}">
                    <tr><th colspan="2" style="{header_style}">Employee Information</th></tr>
                    <tr><td style="{label_style}">Employee Name</td><td style="{value_style}">{instance.employee_name}</td></tr>
                    <tr><td style="{label_style}">Department / Role</td><td style="{value_style}">{instance.department} - {instance.role}</td></tr>
                    <tr><td style="{label_style}">Report Date</td><td style="{value_style}">{instance.date}</td></tr>
                    <tr><td style="{label_style}">Working Hours</td><td style="{value_style}">{instance.start_time} to {instance.end_time} ({instance.total_hours} hrs)</td></tr>

                    <tr><td colspan="2" style="{sub_header}">Task Summary & Metrics</td></tr>
                    <tr>
                        <td colspan="2" style="{value_style}">
                            <table style="width: 100%; text-align: center; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 10px; border-right: 1px solid #eee;"><b>Total</b><br>{instance.tasks_count}</td>
                                    <td style="padding: 10px; border-right: 1px solid #eee; color: green;"><b>Done</b><br>{instance.tasks_done}</td>
                                    <td style="padding: 10px; border-right: 1px solid #eee; color: orange;"><b>Partial</b><br>{instance.tasks_partial}</td>
                                    <td style="padding: 10px; color: red;"><b>Blocked</b><br>{instance.tasks_blocked}</td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr><th colspan="2" style="{header_check if 'header_cell' in locals() else header_style}">Work Details</th></tr>
                    <tr><td style="{label_style}">Task Details</td><td style="{value_style}"><pre style="white-space: pre-wrap; font-family: inherit;">{instance.tasks_text}</pre></td></tr>
                    <tr><td style="{label_style}">Deliverables</td><td style="{value_style}">{instance.deliverables}</td></tr>
                    <tr><td style="{label_style}">Meetings</td><td style="{value_style}"><pre style="white-space: pre-wrap; font-family: inherit;">{instance.meetings_text}</pre></td></tr>
                    <tr><td style="{label_style}">Blockers</td><td style="{value_style}"><span style="color: #d93025;">{instance.blocker_text}</span></td></tr>
                    <tr><td style="{label_style}">Tomorrow's Plan</td><td style="{value_style}">{instance.tomorrow_plan}</td></tr>

                    <tr><td colspan="2" style="{sub_header}">Status & Feedback</td></tr>
                    <tr><td style="{label_style}">Daily Mood</td><td style="{value_style}">{instance.mood_score}/5 {instance.mood_emoji} ({instance.mood_label})</td></tr>
                    <tr><td style="{label_style}">Notes</td><td style="{value_style}">{instance.general_note}</td></tr>
                </table>

                <p style="font-size: 11px; color: #999; text-align: center;">Submitted automatically via Grofession Portal at {instance.submitted_at}</p>
            </div>
        </div>
        """

        recipient_list = [instance.hr_email, 'ceo@grofesion.com']

        try:
            email = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            print("Email Error:", str(e))

        return Response({"status": "success", "message": "EOD Report Submitted & Email Sent Successfully"}, status=status.HTTP_201_CREATED)

    return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





@api_view(["POST"])
def save_questionnaire(request):

    path = request.data.get("business_path")

    print("REQUEST DATA:", request.data)

    if path == "NEW":

        serializer = NewBusinessSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "New Business Saved Successfully"})

        return Response(serializer.errors)

    elif path == "EXISTING":

        serializer = ExistingBusinessSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Existing Business Saved Successfully"})

        return Response(serializer.errors)

    return Response({"error": "Invalid business path"})



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            password = serializer.validated_data['password']

            user = authenticate(request, identifier=identifier, password=password)

            if user:
                login(request, user)
                user_data = UserSerializer(user).data
                return Response({'message': 'Login successful', 'user': user_data})
            else:
                return Response({'non_field_errors': ['Unable to log in with provided credentials.']},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def google_login(request):
    token = request.POST.get('token')
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "1064045400562-lljdlndc03j31gh3e3njeegd4p79ms4l.apps.googleusercontent.com")

        user_email = idinfo['email']
        user_name = idinfo['name']
        # Handle user login / creation here

    except ValueError:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    


@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out"})
    return JsonResponse({"error": "Method not allowed"}, status=405)




class Register(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'User registered successfully!',
                'environment': 'development' if settings.DEBUG else 'production',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Authenticate using email (USERNAME_FIELD = "email")
            user = authenticate(request, email=email, password=password)

            if user is None:
                return Response({
                    "success": False,
                    "message": "Invalid email or password."
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': True,
                'message': 'Login successful!',
                'environment': 'development' if settings.DEBUG else 'production',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ STEP 1: Send OTP
class ForgotPasswordView(APIView):
    """
    POST /api/forgot-password/
    Body: { "email": "user@example.com" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = Users.objects.get(email=email)
                
                # Generate 6-digit OTP
                otp = user.generate_reset_token() # Ensure your User model has this method
                
                # Save OTP and creation time to user model
                user.reset_token = otp
                user.reset_token_created_at = timezone.now()
                user.save()
                
                # Send email
                send_password_reset_email(user, otp)
                
                return Response({
                    'success': True,
                    'message': 'OTP sent successfully to your email.'
                }, status=status.HTTP_200_OK)

            except Users.DoesNotExist:
                # Security: Return success even if email doesn't exist to prevent enumeration
                return Response({
                    'success': True,
                    'message': 'OTP sent successfully to your email.'
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ STEP 2: Verify OTP (New Logic)
class VerifyOtpView(APIView):
    """
    POST /api/verify-otp/
    Body: { "email": "user@example.com", "otp": "123456" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                user = Users.objects.get(email=email)
                
                # 1. Check if OTP matches
                if user.reset_token != otp:
                    return Response({
                        'success': False,
                        'message': 'Invalid OTP. Please try again.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 2. Check if OTP is expired (e.g., valid for 10 minutes)
                expiry_time = user.reset_token_created_at + timedelta(minutes=10)
                if timezone.now() > expiry_time:
                    return Response({
                        'success': False,
                        'message': 'OTP has expired. Please request a new one.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    'success': True,
                    'message': 'OTP Verified Successfully.',
                    'token': otp  # Send back OTP to be used as proof in Step 3
                }, status=status.HTTP_200_OK)

            except Users.DoesNotExist:
                return Response({'success': False, 'message': 'Invalid Email.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ STEP 3: Reset Password
class ResetPasswordView(APIView):
    """
    POST /api/reset-password/
    Body: { 
        "email": "user@example.com",
        "token": "123456", 
        "new_password": "...", 
        "confirm_password": "..." 
    }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            email = request.data.get('email') # Important: Lookup by email, not just token
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = Users.objects.get(email=email)
                
                # Verify Token/OTP one last time before changing password
                if user.reset_token != token:
                     return Response({'success': False, 'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

                # Set new password
                user.set_password(new_password)
                
                # Clear the token so it can't be used again
                user.reset_token = ""
                user.reset_token_created_at = None
                user.save()
                
                return Response({
                    'success': True,
                    'message': 'Password reset successful! You can now login.'
                }, status=status.HTTP_200_OK)
                
            except Users.DoesNotExist:
                return Response({'success': False, 'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginOtpSendView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginOtpSendSerializer(data=request.data)

        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']

            try:
                user = Users.objects.get(phone=mobile, is_active=True)

                otp = user.generate_login_otp()

                # 🔔 SEND OTP VIA SMS (integrate later)
                # send_sms(mobile, f"Your MIBBS login OTP is {otp}")

                return Response({
                    "success": True,
                    "message": "OTP sent to registered mobile number"
                }, status=status.HTTP_200_OK)

            except Users.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Mobile number not registered"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginOtpVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginOtpVerifySerializer(data=request.data)

        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            otp = serializer.validated_data['otp']

            try:
                user = Users.objects.get(phone=mobile, is_active=True)

                # OTP match
                if user.login_otp != otp:
                    return Response({
                        "success": False,
                        "message": "Invalid OTP"
                    }, status=status.HTTP_400_BAD_REQUEST)

                # OTP expiry
                if not user.is_login_otp_valid():
                    return Response({
                        "success": False,
                        "message": "OTP expired"
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Clear OTP after success
                user.clear_login_otp()

                return Response({
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                        "role": user.role.name if user.role else None
                    }
                }, status=status.HTTP_200_OK)

            except Users.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "User not found"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class AssessmentCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AssessmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            assessment = serializer.save()

            # ✅ Prepare email details
            subject = f"New Assessment Submitted: {getattr(assessment, 'business_name', 'Unknown Business')}"
            message = f"""
A new assessment has been submitted.
Submitted By: {getattr(assessment.user, 'username', 'Guest')}
Email: {getattr(assessment.user, 'email', 'N/A')}
Phone: {getattr(assessment.user, 'phone', 'N/A')}
Business Name: {getattr(assessment, 'business_name', '')}
Brand Stage: {getattr(assessment, 'brand_stage', '')}
Industry: {getattr(assessment, 'industry', '')}
City: {getattr(assessment, 'city', '')}, {getattr(assessment, 'state', '')}
Pincode: {getattr(assessment, 'pincode', '')}
Years in Business: {getattr(assessment, 'years_in_business', '')} years {getattr(assessment, 'months_in_business', '')} months
Monthly Revenue: {getattr(assessment, 'monthly_revenue', '')}
Marketing Spend Band: {getattr(assessment, 'marketing_spend_band', '')}
Exact Marketing Spend: {getattr(assessment, 'exact_marketing_spend', '')}
Primary Goals: {getattr(assessment, 'primary_goals', '')}
Competitor Notes: {getattr(assessment, 'competitor_notes', '')}

Monthly Budget: {assessment.monthly_budget}
Annual Budget: {assessment.annual_budget}
PieChart Data: {assessment.piechart_str}



-----------------------------------------
Environment: {"Development" if settings.DEBUG else "Production"}
            """


             # ------- Extract Required Values for Brevo --------
            user = assessment.user
            user_name = getattr(user, "username", "")
            user_email = getattr(user, "email", "")
            user_phone = getattr(user, "phone", "")

            # ------- BREVO Contact add + Email Send --------
            if user_email:
                brevo_result = send_to_brevo(
                    username=user_name,
                    email=user_email,
                    phone=user_phone
                )
                print("BREVO RESULT =>", brevo_result)
            # --------------------------------------------------

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ["magsmenconnect@gmail.com,connect@magsmen.com"],  # 🔹 Change to your admin email
                    fail_silently=False,
                )
            except Exception as e:
                return Response({
                    'success': True,
                    'warning': f"Assessment saved but email failed: {str(e)}",
                    'assessment_id': assessment.id,
                }, status=status.HTTP_201_CREATED)

            return Response({
                'success': True,
                'message': "Assessment created, email sent & Brevo contact added successfully.",
                'assessment_id': assessment.id,
                'environment': 'development' if settings.DEBUG else 'production',
                # 'message': 'Assessment created and email sent successfully.',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class IntalksStatsGet(APIView):
    def get(self, request):
        try:
            stats = Intaklksstatspupdate.objects.last()

            if not stats:
                return Response({"success": False, "message": "No data found"})

            data = {
                "youtubestats": stats.youtubestats,
                "instagramstats": stats.instagramstats,
                "communitygrowthstats": stats.communitygrowthstats,
                "image": stats.image.url if stats.image else None,
                "title": stats.title,
                "description": stats.description,
                "podcasttime": stats.podcasttime,
                "podcastdate": stats.podcastdate,
                "podcastnumber": stats.podcastnumber,
                "guestname": stats.guestname,
                "youtubelink": stats.youtubelink,
                "last_updated": stats.last_updated,
            }

            return Response({
                "success": True,
                "data": data
            })

        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=400
            )
        



class HomeEpisodes(APIView):
    def get(self, request):
        episodes = Intaklksstatspupdate.objects.order_by('-podcastdate')[:3]

        data = []
        for e in episodes:
            data.append({
                "id": e.id,
                "title": e.title,
                "guest": e.guestname,
                "duration": e.podcasttime,
                "thumbnail": request.build_absolute_uri(e.image.url) if e.image else "",
                "description": e.description,
                "youtubeLink": e.youtubelink,
            })

        return Response({"success": True, "data": data})




class AllEpisodes(APIView):
    def get(self, request):
        episodes = Intaklksstatspupdate.objects.all().order_by('-podcastdate')

        data = []
        for item in episodes:
            data.append({
                "id": item.id,
                "title": item.title,
                "guest": item.guestname,
                "duration": item.podcasttime,
                "date": item.podcastdate.strftime("%b %d, %Y") if item.podcastdate else "",
                "category": item.category or "Uncategorized",
                "thumbnail": request.build_absolute_uri(item.image.url) if item.image else "",
                "description": item.description,
                "views": item.podcastviews or "0",
                "youtubeLink": item.youtubelink,
            })

        return Response({"success": True, "data": data})



class AllGuests(APIView):
    def get(self, request):
        # Fetch latest episode for each guest
        latest_ids = (
            Intaklksstatspupdate.objects
            .values('guestname')
            .annotate(latest_id=Max('id'))
            .values_list('latest_id', flat=True)
        )

        episodes = Intaklksstatspupdate.objects.order_by('-podcastdate').filter(id__in=latest_ids)

        data = []
        for e in episodes:
            data.append({
                "id": e.id,
                "guestname": e.guestname or "",
                "thumbnail": request.build_absolute_uri(e.image.url) if e.image else "",
                "youtubeLink": e.youtubelink or "",
                "episodeNumber": e.podcastnumber or "",
                "category": e.category or "Uncategorized",
            })

        return Response({"success": True, "data": data})

def api_view(http_method_names):
    raise NotImplementedError

class api_view:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

def api_view(http_method_names):
    raise NotImplementedError





def youtube_stats(request):
    
    api_key = settings.YOUTUBE_API_KEY
    channel_id = settings.YOUTUBE_CHANNEL_ID

    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "items" not in data or len(data["items"]) == 0:
            return JsonResponse({
                "error": "Invalid response from YouTube API",
                "response": data
            }, status=500)

        stats = data["items"][0]["statistics"]

        return JsonResponse({
            "youtube_views": int(stats.get("viewCount", 0)),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "videos": int(stats.get("videoCount", 0))
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
