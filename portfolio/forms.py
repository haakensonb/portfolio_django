from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': ''}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Message'}), required=True)

