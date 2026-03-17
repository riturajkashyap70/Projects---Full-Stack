from django.core.mail import send_mail
from  django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from defectsapp.models import defects_mod

def send_email_view(email,defect):
    subject='You Have Assigned A New Defect Complete It As Soon As Possible.'
    message='The given defects are assign is in high priority. Please complete it as soon as possible.'
    from_email='karanboss7092al@gmail.com'
    recipient_list=[email]  
   
    #render the HTML email from template
    html_message = render_to_string('defects/task_email_template.html', {'defect': defect})
    #create plain text version by stripping HTML tags
    plain_message = strip_tags(html_message)  
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully.")
    except Exception as e:
        return HttpResponse(f"An error occurred while sending the email: {str(e)}")