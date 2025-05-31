from django import forms
from .models import Bus, Company
#from bootstrap_datepicker_plus import DatePickerInput
#from tempus_dominus.widgets import DateTimePicker
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime



#BUSTYPE = (
#    ("Volvo", "Volvo"),
#    ("Ordinary", "Ordinary"),
#)

BUSFROM = (
    ("From | Aho Uri","From | Aho Uri"),
    ("KIGALI", "KIGALI"),
    ("MUHANGA", "MUHANGA"),
    ("HUYE", "HUYE"),
    ("MUSANZE", "MUSANZE"),
    ("RUBAVU", "RUBAVU"),
    ("NYAMASHEKE", "NYAMASHEKE"),
    ("MUTARA", "MUTARA"),
    ("KAYONZA", "KAYONZA"),
    ("KAMEMBE", "KAMEMBE"),
    ("NYAMATA", "NYAMATA"),
    ("RWAMAGANA", "RWAMAGANA"),
    ("NYAGATARE", "NYAGATARE"),
    ("KARONGI", "KARONGI"),
    ("RUSUMO", "RUSUMO"),
    ("KAGITUMBA", "KAGITUMBA"),
    )

BUSTO = (
    ('To | Aho Ugiye', "To | Aho Ugiye"),
    ("KIGALI", "KIGALI"),
    ("MUHANGA", "MUHANGA"),
    ("HUYE", "HUYE"),
    ("MUSANZE", "MUSANZE"),
    ("RUBAVU", "RUBAVU"),
    ("NYAMASHEKE", "NYAMASHEKE"),
    ("MUTARA", "MUTARA"),
    ("KAYONZA", "KAYONZA"),
    ("KAMEMBE", "KAMEMBE"),
    ("NYAMATA", "NYAMATA"),
    ("RWAMAGANA", "RWAMAGANA"),
    ("NYAGATARE", "NYAGATARE"),
    ("KARONGI", "KARONGI"),
    ("RUSUMO", "RUSUMO"),
    ("KAGITUMBA", "KAGITUMBA"),
    )



class FormFindBus(forms.Form):
    #bus_type = forms.CharField(widget=forms.Select(choices=BUSTYPE), required=True,)
    bus_from = forms.CharField(widget=forms.Select(choices=BUSFROM, attrs={'placeholder': 'From | Aho Uri'}), required=True,)
    bus_to = forms.CharField(widget=forms.Select(choices=BUSTO, attrs={'placeholder': 'To | Aho Ugiye'}), required=True)
    #date = forms.DateField(input_formats=['%d/%m/%Y %H:%M'],required=True)
    #date = forms.DateField(widget = DatePickerInput()) 
    #date = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'),required=True)
    #date = forms.DateTimeField(widget=DateTimePicker(),initial='1980-01-01 12:00:00',)
    date = forms.DateField(widget=AdminDateWidget())
    time = forms.DateField(widget=AdminTimeWidget())
    #date_time = forms.DateField(widget=AdminSplitDateTime())

    
    #def clean(self):
    #    if "bus_from" in self.cleaned_data and "bus_to" in self.cleaned_data and self.cleaned_data["bus_from"] == self.cleaned_data["bus_to"]:
    #        raise forms.ValidationError("From and To are same")
    #    return self.cleaned_data
    
class BusCreateForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ["type_of_bus", "plate_number","slug","location_from",'location_to', "seats","ticket_price", "available","departure_date","departure_time","arrival_date","arrival_time","image"]

        widgets = {
        "departure_date":  forms.DateInput(attrs={'class':'form-control','type':'date'}),"departure_time" :  forms.TimeInput(attrs={'class':'timepicker','type':'time'}) ,"arrival_date":  forms.DateInput(attrs={'class':'form-control','type':'date'}), "arrival_time" :  forms.TimeInput(attrs={'class':'form-control','type':'time'}) }

        prepopulated_fields = {'slug': ('bus_company','plate_number')}

class BusUpdateForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ["location_from",'location_to',"ticket_price", "available","departure_date","departure_time","arrival_date","arrival_time","image"]

        widgets = {
        "departure_date":  forms.DateInput(attrs={'class':'form-control','type':'date'}),"departure_time" :  forms.TimeInput(attrs={'class':'form-control','type':'time'}) ,"arrival_date":  forms.DateInput(attrs={'class':'form-control','type':'date'}), "arrival_time" :  forms.TimeInput(attrs={'class':'form-control','type':'time'}) }




class CompanyCreateForm(forms.ModelForm):
    class Meta:
    	email = forms.EmailField()
    	model = Company
    	fields = ["name","contact_person","phone","email","address","description","logo","ratings"]


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        email = forms.EmailField()
        model = Company
        fields = ["name","contact_person","phone","email","address","description","logo","ratings"]