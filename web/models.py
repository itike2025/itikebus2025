from django.db import models
from django.core.exceptions import ValidationError
from comment.models import Comment
#from django.utils.translation import ugettext_noop
from django.utils.translation import gettext_noop
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from six import python_2_unicode_compatible



class Tag(models.Model):
    word = models.CharField(max_length=35)
    slug = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.word

    def __str__(self):
        return self.word


class Company(models.Model):
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=35)
    slug = models.CharField(max_length=250)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=2000)
    contact_person = models.CharField(max_length=2000)
    phone = models.IntegerField()
    email = models.EmailField(max_length=2000)
    address = models.CharField(max_length=2000)
    logo = models.ImageField(upload_to='company/%Y/%m/%d', blank=True)
    cliked = models.ManyToManyField(User, related_name='cliked',default=None,blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    available = models.BooleanField(default=False)

    comments = GenericRelation(Comment)
    RATING_CHOICE = (
        ('1', gettext_noop('Worst')),
        ('2', gettext_noop('Bed')),
        ('3', gettext_noop('Average')),
        ('4', gettext_noop('Good')),
        ('5', gettext_noop('Best')),
    )
    ratings = models.CharField(
        blank=True, null=True, max_length=1, db_index=True, choices=RATING_CHOICE
    )


    def __str__(self):
        return self.name



#class Route(models.Model):
#    class Meta:
#        verbose_name_plural = "Routes"
#        
#    BUSFROM = (
#    ('Delhi', 'Delhi'),
#    ('Jaipur', 'Jaipur'),
#    ('Ajmer', 'Ajmer'),
#    )

#    BUSTO = (
#    ('Ajmer', 'Ajmer'),
#    ('Chandigarh', 'Chandigarh'),
#    ('Delhi', 'Delhi'),
#    )
    
#    route_id = models.AutoField(primary_key=True,)    
#    location_from = models.CharField(max_length=255, choices=BUSFROM)
#    location_to = models.CharField(max_length=255,choices=BUSTO)        
    
#    def __str__(self):
#        if self.location_from == self.location_to:
#            raise ValidationError('To and From Can\'t be the same')
#        return '{0}-{1}'.format(str(self.location_from), str(self.location_to))

#class Route(models.Model):


BUSFROM = (
    ('KIGALI', 'KIGALI'),
    ('MUHANGA', 'MUHANGA'),
    ('HUYE', 'HUYE'),
    ('MUSANZE', 'MUSANZE'),
    ('RUBAVU', 'RUBAVU'),
    ('NYAMASHEKE', 'NYAMASHEKE'),
    ('MUTARA', 'MUTARA'),
    ('KAYONZA', 'KAYONZA'),
    ('KAMEMBE', 'KAMEMBE'),
    ('NYAMATA', 'NYAMATA'),
    ('RWAMAGANA', 'RWAMAGANA'),
    ('NYAGATARE', 'NYAGATARE'),
    ('KARONGI', 'KARONGI'),
    ('RUSUMO', 'RUSUMO'),
    ('KAGITUMBA', 'KAGITUMBA'),
    )

BUSTO = (

    ('KIGALI', 'KIGALI'),
    ('MUHANGA', 'MUHANGA'),
    ('HUYE', 'HUYE'),
    ('MUSANZE', 'MUSANZE'),
    ('RUBAVU', 'RUBAVU'),
    ('NYAMASHEKE', 'NYAMASHEKE'),
    ('MUTARA', 'MUTARA'),
    ('KAYONZA', 'KAYONZA'),
    ('KAMEMBE', 'KAMEMBE'),
    ('NYAMATA', 'NYAMATA'),
    ('RWAMAGANA', 'RWAMAGANA'),
    ('NYAGATARE', 'NYAGATARE'),
    ('KARONGI', 'KARONGI'),
    ('RUSUMO', 'RUSUMO'),
    ('KAGITUMBA', 'KAGITUMBA'),
    )

    
    #route_id = models.AutoField(primary_key=True,)    
    #location_from = models.CharField(max_length=255)
    #location_to = models.CharField(max_length=255)  
    #location_from = models.CharField(max_length=255, choices=BUSFROM)
    #location_to = models.CharField(max_length=255,choices=BUSTO)         
    
    #def __str__(self):
    #    if self.location_from == self.location_to:
    #        raise ValidationError('To and From Can not be the same')
    #    return '{0} to {1}'.format(str(self.location_from), str(self.location_to))

    #class Meta:
    #    ordering = ('route_id',)
    #    verbose_name_plural = "Routes"
    #    index_together = (('location_from', 'location_to'),)


        
# @python_2_unicode_compatible
# class Bus(models.Model):
    
#     BUSTYPE = (
#     ('--', '--'),
#     ('TOYOTA COASTER', 'TOYOTA COASTER'),
#     ('TOYOTA HIACE', 'TOYOTA HIACE'),
#     ('BENZ BUS', 'BENZ BUS'),
#     ('VOLVO BUS', 'VOLVO BUS'),
#     ('HYUNDAI BUS','HYUNDAI BUS'),
#     )
	
    
	
#     class Meta:
#         verbose_name_plural = "Buses"
#     id = models.AutoField(primary_key=True,)
#     plate_number = models.CharField(max_length=20,unique=True)
#     bus_company = models.ForeignKey(Company,on_delete=models.CASCADE)
#     type_of_bus = models.CharField(max_length=255, choices=BUSTYPE)
#     ticket_price = models.IntegerField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     departure_date = models.DateField(null=True)
#     departure_time = models.TimeField(null=True)
#     arrival_date = models.DateField(null=True)
#     arrival_time = models.TimeField(null=True)
#     #route = models.ForeignKey(Route,on_delete=models.CASCADE)
#     location_from = models.CharField(max_length=255, choices=BUSFROM,default='KIGALI')
#     location_to = models.CharField(max_length=255,choices=BUSTO,default='KIGALI')     
#     seats = models.PositiveSmallIntegerField(default=1, verbose_name="Number of seats")
#     #seatd = models.CharField(max_length=100,default=None,blank=True,null=True)
#     #jseats = models.JSONField(default=None,blank=True,null=True)
#     image = models.ImageField(upload_to='bus/%Y/%m/%d', blank=True)
#     slug = models.SlugField()
#     available = models.BooleanField(default=True)

#     liked = models.ManyToManyField(User, related_name='liked',default=None,blank=True)
#     hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
#     comments = GenericRelation(Comment)
#     RATING_CHOICE = (
#         ('1', gettext_noop('Worst')),
#         ('2', gettext_noop('Bed')),
#         ('3', gettext_noop('Average')),
#         ('4', gettext_noop('Good')),
#         ('5', gettext_noop('Best')),
#     )
#     ratings = models.CharField(
#         blank=True, null=True, max_length=1, db_index=True, choices=RATING_CHOICE
#     )
    

#     Tags = models.ManyToManyField(Tag,related_name='bus_details', blank=False)

#     def __str__(self):
#         return '{0}:{1}:{2}:{3}:{4}'.format(self.bus_company,self.type_of_bus,str(self.plate_number), self.route, self.departure_date)
    
#     class Meta:
#         ordering = ('created',)
#         verbose_name_plural = "buses"
#         index_together = (('id', 'slug','location_from', 'location_to'),)


#     def get_absolute_url(self):
#         return reverse('bus_detail',args=[self.id, self.slug])

#     #def __init__(self, *args, **kwargs):
#     #    super().__init__(*args, **kwargs)
#     #    if self.seatd:
#     #        self.seatd= eval(self.seatd)

#     def __str__(self):
#         if self.location_from == self.location_to:
#             raise ValidationError('To and From Can not be the same')
#         return '{0} to {1}'.format(str(self.location_from), str(self.location_to))



@python_2_unicode_compatible
class Bus(models.Model):

    BUSTYPE = (
        ('--', '--'),
        ('TOYOTA COASTER', 'TOYOTA COASTER'),
        ('TOYOTA HIACE', 'TOYOTA HIACE'),
        ('BENZ BUS', 'BENZ BUS'),
        ('VOLVO BUS', 'VOLVO BUS'),
        ('HYUNDAI BUS','HYUNDAI BUS'),
    )

    RATING_CHOICE = (
        ('1', gettext_noop('Worst')),
        ('2', gettext_noop('Bad')),
        ('3', gettext_noop('Average')),
        ('4', gettext_noop('Good')),
        ('5', gettext_noop('Best')),
    )

    id = models.AutoField(primary_key=True)
    plate_number = models.CharField(max_length=20, unique=True)
    bus_company = models.ForeignKey('Company', on_delete=models.CASCADE)
    type_of_bus = models.CharField(max_length=255, choices=BUSTYPE)
    ticket_price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    departure_date = models.DateField(null=True)
    departure_time = models.TimeField(null=True)
    arrival_date = models.DateField(null=True)
    arrival_time = models.TimeField(null=True)
    location_from = models.CharField(max_length=255, choices=BUSFROM, default='KIGALI')
    location_to = models.CharField(max_length=255, choices=BUSTO, default='KIGALI')
    seats = models.PositiveSmallIntegerField(default=1, verbose_name="Number of seats")
    image = models.ImageField(upload_to='bus/%Y/%m/%d', blank=True)
    slug = models.SlugField()
    available = models.BooleanField(default=True)
    liked = models.ManyToManyField(User, related_name='liked', default=None, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    comments = GenericRelation(Comment)
    ratings = models.CharField(
        blank=True, null=True, max_length=1, db_index=True, choices=RATING_CHOICE
    )
    Tags = models.ManyToManyField(Tag, related_name='bus_details', blank=False)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = "Buses"
        indexes = [
            models.Index(fields=['id', 'slug', 'location_from', 'location_to']),
        ]

    def __str__(self):
        if self.location_from == self.location_to:
            raise ValidationError('To and From cannot be the same')
        return '{0} to {1}'.format(str(self.location_from), str(self.location_to))

    def get_absolute_url(self):
        return reverse('bus_detail', args=[self.id, self.slug])






class Seatsall(models.Model):
    #SEATS_CHOICES =( 
    #("0", "0"),
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
    #("11", "11"), 
    #("12", "12"), 
    #("13", "13"), 
    #("14", "14"), 
    #("15", "15"),
    #("16", "16"), 
    #("17", "17"), 
    #("18", "18"), 
    #("19", "19"), 
    #("20", "20"), 
    #("21", "21"), 
    #("22", "22"), 
    #("23", "23"), 
    #("24", "24"), 
    #("25", "25"),
    #("26", "26"), 
    #("27", "27"), 
    #("28", "28"), 
    #("29", "29"), 
    #("30", "30"), 
    #("31", "31"), 
    #("32", "32"), 
    #("33", "33"), 
    #("34", "34"), 
    #("35", "35"),
    #("36", "36"), 
    #("37", "37"), 
    #("38", "38"), 
    #("39", "39"), 
    #("40", "40"), 
    #("41", "41"), 
    #("42", "42"), 
    #("43", "43"), 
    #("44", "44"), 
    #("45", "45"),
    #("46", "46"), 
    #("47", "47"), 
    #("48", "48"), 
    #("49", "49"), 
    #("50", "50"), ) 

    #select_seats = models.CharField(choices=SEATS_CHOICES, default='0', max_length=10)
    seatlabel = models.CharField(max_length = 10,null=True,default='seat')
    available = models.BooleanField(default=True,null=True)
    seatbus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def disable(self):
    	self.available = False
    	self.save()

    def enable(self):
    	self.available = True
    	self.save()
    

    def __str__(self):
    	return self.seatlabel+'___:'+self.seatbus.type_of_bus+':'+self.seatbus.plate_number


def create_seats(sender, **kwargs):
	if kwargs['created']:
		#seats = Seatsall.objects.bulk_create([Seatsall(seatlabel=x) for x in range(1, 50)],seatbus = kwargs['instance'])
		#seatbus = Seatsall.objects.create(seatbus = kwargs['instance'])
		vs = kwargs.get('instance').seats
		#print(vs)
		print('kwargs:',kwargs)
		print('kw2:',kwargs['instance'])
		for i in range(1,vs+1):
			kwargs['instance'].seatlabel= str(i)
			seatbus = Seatsall.objects.create(seatlabel = str(i),seatbus = kwargs['instance'])


post_save.connect(create_seats, sender=Bus)

    

    #def builtin():
    #insert_list = []
    #for i in range(10000):
    #    name="String number %s" %i
    #    insert_list.append(Record(name=name))
    #Record.objects.bulk_create(insert_list)



