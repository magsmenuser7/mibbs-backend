from sib_api_v3_sdk import ApiClient, Configuration, ContactsApi, TransactionalEmailsApi
from sib_api_v3_sdk.models import CreateContact, SendSmtpEmail
from django.conf import settings

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
