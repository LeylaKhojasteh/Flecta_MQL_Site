from django import forms
from website.models import Contact
from captcha.fields import CaptchaField


class NameForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField( max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)



PROJECT_TYPE_CHOICES = [
    ("", "Select a service"),
    ("expert-advisor", "Custom Expert Advisor"),
    ("indicator", "Custom Indicator"),
    ("strategy-automation", "Strategy Automation"),
    ("debugging", "MQL Code Debugging"),
    ("migration", "MQL4 to MQL5 Migration"),
    ("consultation", "Technical Consultation"),
    ("other", "Other"),
]


PLATFORM_CHOICES = [
    ("", "Select a platform"),
    ("mt4", "MetaTrader 4"),
    ("mt5", "MetaTrader 5"),
    ("both", "MetaTrader 4 and 5"),
    ("tradingview", "TradingView"),
    ("not-sure", "Not sure yet"),
]


class ContactForm(forms.Form):
    full_name = forms.CharField(
        label="Full Name",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your full name",
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        ),
    )

    project_type = forms.ChoiceField(
        label="Project Type",
        choices=PROJECT_TYPE_CHOICES,
        widget=forms.Select(),
    )

    platform = forms.ChoiceField(
        label="Trading Platform",
        choices=PLATFORM_CHOICES,
        widget=forms.Select(),
    )

    subject = forms.CharField(
        label="Project Subject",
        max_length=200,
        widget=forms.TextInput(
            attrs={"placeholder": ("Example: Custom risk management Expert Advisor"
                ),
            }
        ),
    )

    message = forms.CharField(
        label="Project Description",
        min_length=20,
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": (
                    "Describe your strategy, entry and exit rules, "
                    "risk management requirements, or any other "
                    "important details..."
                ),
            }
        ),
    )

    agreement = forms.BooleanField(
        label=(
            "I understand that project pricing and delivery time "
            "depend on the final requirements."
        ),
        required=True,
    )

    captcha = CaptchaField(
        label="Security Check",
    )
    
    
    
