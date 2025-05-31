from django import forms
from .models import Order
from web.models import Seatsall



class CartForm(forms.Form):
    #SEATS_CHOICES =( 
    #("1", "1"), 
    #("2", "2"), 
    #("3", "3"), 
    #("4", "4"), 
    #("5", "5"),
    #("6", "6"), 
    #("7", "7"), 
    #("8", "8"), 
    #("9", "9"), 
    #("10", "10"), 
#) 
    quantity = forms.IntegerField(initial='1')
    bus_id = forms.IntegerField(widget=forms.HiddenInput)
    seatd = forms.IntegerField(widget=forms.HiddenInput)
    #seats = forms.ChoiceField(widget=forms.Select, choices=SEATS_CHOICES)
    #seatd = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=SEATS_CHOICES)
    #seatd = forms.ModelMultipleChoiceField(queryset=Seatsall.objects.filter(available=True),widget=forms.CheckboxSelectMultiple)
    #check_id = forms.ModelChoiceField(queryset=Bus.objects.all(),widget=forms.CheckboxSelectMultiple)
    #seatd = forms.ModelMultipleChoiceField(queryset=show_bus.seats,widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Seatsall
        fields = ['seatlabel',]
        exclude = ['seatbus']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CartForm, self).__init__(*args, **kwargs)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        #exclude = ('paid','user')
        fields =['name','email','postal_code','address']

        widgets = {
            'address': forms.Textarea(attrs={'row': 5, 'col': 8}),
        }