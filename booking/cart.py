from .models import CartItem
from web.models import Bus, Seatsall
from django.shortcuts import get_object_or_404, get_list_or_404
#from itertools import imap


def _cart_id(request):
    if 'cart_id' not in request.session:
        request.session['cart_id'] = _generate_cart_id()

    return request.session['cart_id']


def _generate_cart_id():
    import string, random
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(50)])


def get_all_cart_items(request):
    return CartItem.objects.filter(cart_id = _cart_id(request))


def add_item_to_cart(request):
    # cart_id = _cart_id(request)

    bus_id = request.form_data['bus_id']
    quantity = request.form_data['quantity']
    #seats = request.form_data['seatd']
    seats2 = request.POST.getlist('seatd')
    seats1 = list(filter(None, seats2))
    seats_number =''
    for seat in seats1:
        cs = Seatsall.objects.get(id=seat)
        #print('cs_labels',cs.seatlabel)
        seats_number += cs.seatlabel + ','
        Seatsall.disable(cs)

    #print('s',seats)
    #seats = '\n'.join(seats)
    #seats = str(seats.strip('[]'))
    #seats = ' ,'.join(map(str, seats1))
    #seats = ",".join(imap(str, l))
    #seats = ",".join([str(item) for item in seats1])
    #seats = '\n'.join(request.form_data['seatd'])
    #quantity = 1
    seats= ''
    for seat in seats1:
        seats += seat + ','

    p = get_object_or_404(Bus, id=bus_id)

    price = p.ticket_price

    cart_items = get_all_cart_items(request)

    item_in_cart = False

    for cart_item in cart_items:
        if cart_item.bus_id == bus_id:
            cart_item.update_quantity(quantity)
            #cart_item.update_seats(seats)
            #print('seats',seats)
            for s in seats1:
                sl = Seatsall.objects.get(id=s)
                cart_item.update_seats(s + ',')
                cart_item.update_seatsnumber(sl.seatlabel + ',')

            #cart_item.seats= seats
            # cart_item.save()
            item_in_cart = True

    if not item_in_cart:
        item = CartItem(
            cart_id = _cart_id(request),
            price = price,
            quantity = quantity,
            bus_id = bus_id,
            seats = seats,
            seats_number= seats_number,
            
        )

        # item.cart_id = cart_id
        item.save()


def item_count(request):
    return get_all_cart_items(request).count()


def subtotal(request):
    cart_item = get_all_cart_items(request)
    sub_total = 0
    for item in cart_item:
        sub_total += item.total_cost()

    return sub_total


def remove_item(request):
    item_id = request.POST.get('item_id')
    ci = get_object_or_404(CartItem, id=item_id)

    #for seat in ci.seats:
        #cs = Seatsall.objects.get(id=seat)
        #print('cs',seat)
        #Seatsall.enable(cs)
    #lseats = list(filter(None, ci.seats))
    #seatids = [int(i) for i in lseats.split(',')]
    seatids = [i for i in ci.seats.split(',')]
    #seatids = [int(i) for i in lseats]
    #print(seatids)
    for seatid in seatids[:-1:]:
        se = Seatsall.objects.get(id= int(seatid))
        #print('sid :',seatid)
        Seatsall.enable(se)

    ci.delete()


def update_item(request):
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantity')
    ci = get_object_or_404(CartItem, id=item_id)
    if quantity.isdigit():
        quantity = int(quantity)
        ci.quantity = quantity
        ci.save()


def clear(request):
    cart_items = get_all_cart_items(request)
    cart_items.delete()


