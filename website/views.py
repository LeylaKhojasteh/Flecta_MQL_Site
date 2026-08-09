from dataclasses import fields

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from website.forms import NameForm,ContactForm, NewsletterForm
from django.contrib import messages

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

            # اینجا منطق قبلی خودت را قرار بده.
            # مثلاً:
            # 1. ذخیره داخل دیتابیس
            # 2. ارسال ایمیل
            # 3. ثبت درخواست پروژه

            print("Full name:", full_name)
            print("Email:", email)
            print("Project type:", project_type)
            print("Platform:", platform)
            print("Subject:", subject)
            print("Message:", message)

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


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()

    return HttpResponseRedirect('/')


def test_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            print('true')
        else:
            print('false')

    form = ContactForm()
    return render(request,'test.html',{'form':form})
