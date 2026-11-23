from django import forms
from blog.models import Comment
from captcha.fields import CaptchaField



class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
    captcha = CaptchaField(label='Security Check')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None and user.is_authenticated:
            self.fields.pop('name')
            self.fields.pop('email')

    class Meta:
        model = Comment
        fields = ['name', 'email', 'subject', 'message']
        