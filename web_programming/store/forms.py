from django import forms
import datetime
from django.forms.widgets import NumberInput
from django.contrib.admin import widgets


class BuyForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=50)

class UpdateForm(forms.Form):
    update_quantity = forms.IntegerField(initial=0, min_value=0, max_value=50)

class PaymentForm(forms.Form):
    BANK_SCB = 'S'
    BANK_KBANK = 'K'
    BANK_KRUNGTHAI = 'T'
    BANK_CHOICES = [
        (BANK_SCB,'SCB'),
        (BANK_KBANK,'KBank'),
        (BANK_KRUNGTHAI,'KrungThai'),
    ]
    bank = forms.ChoiceField(choices=BANK_CHOICES)
    datetime = forms.DateTimeField(initial=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    slip = forms.ImageField()

class BookingForm(forms.Form):
    PEOPLE_2 = '2'
    PEOPLE_4 = '4'
    PEOPLE_CHOICES = [
        (PEOPLE_2,'2 persons'),
        (PEOPLE_4,'4 persons'),
    ]
    checkin = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    checkout = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    people = forms.ChoiceField(choices=PEOPLE_CHOICES)
