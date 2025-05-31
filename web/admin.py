from django.contrib import admin
from .models import Bus,Tag,Company,Seatsall




class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('word',)}


class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_company','type_of_bus', 'plate_number','slug','location_from','location_to', 'seats','ticket_price', 'available','departure_date','departure_time','arrival_date','arrival_time' ]
    list_filter = ['bus_company','location_from','location_to','available','departure_date','departure_time','arrival_date','arrival_time']
    list_editable = ['ticket_price', 'available','departure_date','departure_time','arrival_date','arrival_time','seats']
    search_fields = ['bus_company']
    prepopulated_fields = {'slug': ('bus_company','plate_number')}

admin.site.register(Bus, BusAdmin)

class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

#admin.site.register(Route)
admin.site.register(Seatsall)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Tag, TagAdmin)
