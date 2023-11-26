from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_email(self, subject: str, message: str, from_email: str, to_email: list[str]) -> None:
        print(subject, message, from_email, to_email)