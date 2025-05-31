from django.db import models
from django.contrib.auth.models import User
from web.models import Bus











#class Seat(models.Model):
#	car = models.ForeignKey(Car, related_name='car_seats',on_delete=models.CASCADE)
	# function to create seats
#	@receiver(post_save, sender=Car)
#	def create_seats(sender, instance, created, **kwargs):
#		if created:
#			for seat in range (0, instance.seats):
#				instance.seat_set.create()



#SEAT_CHOICES = (
#        ('1', '1'),
#       ('3', '3'),
#       ('4', '4'),
#       ('5', '5'),
#        ('6', '6')
#    )
#class Seat(models.Model):
#	car = models.ForeignKey(Car, related_name='carseats',on_delete=models.CASCADE)
#    #user = models.ForeignKey(User, on_delete=models.CASCADE)
#    #seatticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#	seat_detail = models.CharField(choices=SEAT_CHOICES,default='-', max_length=2)

#	def __str__(self):
#		return str(self.seat_detail) 

#class Seat(Enum):
#    AA = 1
#    AB = 2
#    BA = 3
#    BB = 4
#    CA = 5
#    CB = 6

#class CarSeat(models.Model):
#	car = models.ForeignKey(Car, related_name='car_s',on_delete=models.CASCADE)

#    there 6 seats in a hall

    #number_seats = models.PositiveIntegerField()
    #seat = models.CharField(choices=SEAT_CHOICES, max_length=2)
#	seat = range(0,car.seats)

#	def __str__(self):
#		return self.seat



LIKE_CHOICES = (

            ('Like','Like'),
            ('Unlike','Unlike'),
        )

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.bus)


class CartItem(models.Model):
    #user = models.ForeignKey(User, related_name='ucart', on_delete=models.SET_NULL, null=True)
    cart_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    seats = models.CharField(max_length=200,null=True,blank=True)
    seats_number = models.CharField(max_length=200,null=True,blank=True)


    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def update_seats(self, seats):
        self.seats = self.seats + str(seats)
        self.save()
        #self.seats = []
        #self.append(seats)
        #self.save()

    def update_seatsnumber(self, seats_number):
        self.seats_number = self.seats_number + str(seats_number)
        self.save()


    def total_cost(self):
        return self.quantity * self.price


class Order(models.Model):
    user = models.ForeignKey(User, related_name='uorders', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=191,default=None)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=191)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.name, self.date)

    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ] )


class LineItem(models.Model):
    user = models.ForeignKey(User, related_name='uitems', on_delete=models.SET_NULL, null=True)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(self.price, self.id)

    def cost(self):
        return self.price * self.quantity



class Slider(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sliders/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.name