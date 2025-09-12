from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
from .models import EmailLog
from django.contrib.auth.decorators import login_required
import requests

def home(request):
    return render(request, 'home.html')
@login_required
def send_email(request):
    result_message = ""
    if request.method == "POST":
        to_email = request.POST.get('to')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        uploaded_files = request.FILES.getlist('attachments')

        email = EmailMessage(
            subject,
            None,
            settings.EMAIL_HOST_USER,
            [to_email],
        )
        email.content_subtype = "html"
        email.body = message

        for uploaded_file in uploaded_files:
            email.attach(
                uploaded_file.name,
                uploaded_file.read(),
                uploaded_file.content_type
            )
        try:
            email.send(fail_silently=False)
            result_message = f"Email sent successfully to {to_email}"
        except Exception as e:
            result_message = f"Error sending email: {str(e)}"

        return render(request, 'send_email.html', {'message': result_message})

    return render(request, 'send_email.html')


def about(request):
    return render(request, 'about.html')



@login_required
def ai_generate_email(request):
    generated_email = None

    if request.method == "POST":
        prompt = request.POST.get('prompt')

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert email copywriter."},
                {"role": "user", "content": f"Write a professional email for: {prompt}"}
            ],
            "temperature": 0.7,
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            generated_email = result["choices"][0]["message"]["content"]
        else:
            generated_email = f"Error from OpenAI API: {result.get('error', {}).get('message', 'Unknown error')}"

    return render(request, 'ai_email.html', {'generated_email': generated_email})
