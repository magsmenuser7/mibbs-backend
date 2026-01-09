from sib_api_v3_sdk import ApiClient, Configuration, ContactsApi, TransactionalEmailsApi
from sib_api_v3_sdk.models import CreateContact, SendSmtpEmail
from django.core.mail import send_mail
from django.conf import settings


# brevo related functionality 
def send_to_brevo(email, username="", phone=""):
    """Create contact + send welcome email using template"""

    # ✅ Correct way to configure API key
    configuration = Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    api_client = ApiClient(configuration)

    # 1️⃣ Create Brevo Contact
    # numbers = [num.strip() for num in phone.split(",") if num.strip()]
    # phone = ", ".join(numbers)
    contacts_api = ContactsApi(api_client)
    new_contact = CreateContact(
        email=email,
        attributes={"FIRSTNAME": username, "PHONE": phone},
        list_ids=[5]  # 🔹 Replace with your list ID
    )
    contacts_api.create_contact(new_contact)

    # 2️⃣ Send SMTP Welcome Email
    transactional_api = TransactionalEmailsApi(api_client)
    smtp_email = SendSmtpEmail(
        to=[{"email": email, "name": username}],
        template_id=1,  # 🔹 Replace with your welcome email template ID
        params={"name": username}
    )
    transactional_api.send_transac_email(smtp_email)
    return {"status": "Contact created and welcome email sent"}







# forgotpassword  related functionality  


def send_password_reset_email(user, reset_token):
    """
    Send password reset email with 6-digit token to user
    """
    subject = '🔐 Password Reset Request - MIBBS'
    
    # Plain text message
    message = f"""
Hello {user.username},

You have requested to reset your password for your MIBBS account.

Your 6-digit password reset code is:

    {reset_token}

This code will expire in 24 hours.

To reset your password:
1. Copy the 6-digit code above
2. Go back to the password reset page
3. Enter your code and new password

If you did not request this password reset, please ignore this email or contact our support team.

Best regards,
MIBBS Team
    """
    
    # HTML message with better styling
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9fafb;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 32px; font-weight: bold;">MIBBS</h1>
            </div>
            
            <div style="background-color: white; padding: 40px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="color: #1F2937; margin-top: 0; font-size: 24px;">🔐 Password Reset Request</h2>
                
                <p style="color: #4B5563; font-size: 16px; line-height: 1.6;">
                    Hello <strong style="color: #1F2937;">{user.username}</strong>,
                </p>
                
                <p style="color: #4B5563; font-size: 16px; line-height: 1.6;">
                    You have requested to reset your password for your MIBBS account.
                </p>
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; margin: 30px 0; text-align: center;">
                    <p style="margin: 0 0 15px 0; font-size: 14px; color: #fff; opacity: 0.95; text-transform: uppercase; letter-spacing: 1px;">
                        Your Reset Code
                    </p>
                    <div style="background-color: rgba(255, 255, 255, 0.2); padding: 20px; border-radius: 8px; display: inline-block;">
                        <p style="margin: 0; font-size: 48px; font-weight: bold; color: #fff; letter-spacing: 8px; font-family: 'Courier New', monospace;">
                            {reset_token}
                        </p>
                    </div>
                </div>
                
                <div style="background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0; font-size: 14px; color: #92400E;">
                        <strong>⏰ Important:</strong> This code will expire in 24 hours for security reasons.
                    </p>
                </div>
                
                <div style="background-color: #F3F4F6; padding: 25px; border-radius: 8px; margin: 25px 0;">
                    <p style="margin: 0 0 15px 0; font-weight: bold; color: #1F2937; font-size: 16px;">
                        📝 How to reset your password:
                    </p>
                    <ol style="margin: 0; padding-left: 20px; color: #4B5563; line-height: 1.8;">
                        <li style="margin-bottom: 10px;">Copy the 6-digit code above</li>
                        <li style="margin-bottom: 10px;">Go back to the password reset page</li>
                        <li>Enter your code and choose a new password</li>
                    </ol>
                </div>
                
                <div style="background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 15px 20px; margin: 25px 0; border-radius: 4px;">
                    <p style="margin: 0; font-size: 14px; color: #1E40AF;">
                        <strong>🛡️ Security Tip:</strong> If you didn't request this password reset, please ignore this email or contact our support team immediately.
                    </p>
                </div>
                
                <p style="color: #6B7280; font-size: 14px; line-height: 1.6; margin-top: 30px;">
                    Need help? Contact our support team at <a href="mailto:support@mibbs.ai" style="color: #667eea; text-decoration: none;">support@mibbs.ai</a>
                </p>
                
                <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 30px 0;">
                
                <div style="text-align: center; color: #9CA3AF; font-size: 12px;">
                    <p style="margin: 5px 0;">Best regards,</p>
                    <p style="margin: 5px 0; font-weight: bold; color: #667eea; font-size: 14px;">The MIBBS Team</p>
                    <p style="margin: 20px 0 5px 0;">© 2024 MIBBS. All rights reserved.</p>
                    <p style="margin: 5px 0;">
                        <a href="#" style="color: #9CA3AF; text-decoration: none; margin: 0 10px;">Privacy Policy</a> | 
                        <a href="#" style="color: #9CA3AF; text-decoration: none; margin: 0 10px;">Terms of Service</a>
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"✅ Password reset email sent successfully to {user.email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email to {user.email}: {str(e)}")
        return False