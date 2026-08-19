from dataclasses import fields

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from website.forms import NameForm,ContactForm
from django.contrib import messages
from website.models import Contact
from django.conf import settings
from django.core.mail import EmailMessage


def home_view(request):
    return render(request,'website/home.html')


def coming_soon_view(request, url=None):
    return render(request, 'website/coming-soon.html')


def about_view(request):
    return render(request,'website/about.html')

# 

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            project_type = form.cleaned_data["project_type"]
            platform = form.cleaned_data["platform"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            Contact.objects.create(
                name=full_name,
                email=email,
                project_type=project_type,
                platform=platform,
                subject=subject,
                message=message,
                )

            email_message = EmailMessage(
                    subject=f"New project request: {subject}",
                    body=(
                        f"Name: {full_name}\n"
                        f"Email: {email}\n"
                        f"Project type: {project_type}\n"
                        f"Platform: {platform}\n\n"
                        f"Message:\n{message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECIPIENT_EMAIL],
                    reply_to=[email],
                )

            email_message.send(fail_silently=False)

            messages.success(
                request,
                "Your project request has been submitted successfully.",
            )

            # جلوگیری از ارسال دوباره فرم بعد از Refresh
            return redirect("website:contact")

    else:
        form = ContactForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "website/contact.html",
        context,
    )


