from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import  Order, LineItem,Like, Slider
from web.models import  Bus,Tag, Company,Seatsall
from .forms import CartForm, CheckoutForm
from . import cart

from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

# Create your views here.
'''
def cindex(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    productsall = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        productsall = productsall.filter(category=category)

    page = request.GET.get('page', 1)

    paginator = Paginator(productsall, 5)
    try:
        all_products = paginator.page(page)
    except PageNotAnInteger:
        all_products = paginator.page(1)
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)
    return render(request,"ecommerce_app/cindex.html",{'category':category,'categories':categories, 'all_products':all_products})
'''
def index(request):
    ## Your code here.
    #carousel = Slider.objects.get(pk=1)
    carousel = Slider.objects.all()
    return render( request,'booking/index.html',{'carousel': carousel, })

def index1(request):
    #products = Product.objects.all()
    buses = Bus.objects.filter(available=True).order_by('-created')
    #companies = Company.objects.all()
    companies = Company.objects.filter(available=True).order_by('-created')
    #products = Product.objects.all().order_by('-created')

    # if user need to filter products otherwise list all products
    #category = None
    #routes = Route.objects.all()
    #productsall = Product.objects.filter(available=True)
    #if category_slug:
        #category = get_object_or_404(Category, slug=category_slug)
        #productsall = productsall.filter(category=category)



    if request.method == "POST":

        # Filter criteria
        search_query = request.POST.get("search_query", None)
        min_price = request.POST.get("min_price", None)
        max_price = request.POST.get("max_price", None)
        rating = request.POST.get("rating", None)
        tag = request.POST.get("tag", None)
        #route = request.POST.get("route", None)
        company = request.POST.get("company", None)

    
        if min_price:
            buses = buses.filter(ticket_price__gte = min_price)
        if max_price:
            buses = buses.filter(ticket_price__lte = max_price)
        if rating and rating != "-":
            buses = buses.filter(ratings = rating)
        if tag and tag != "-":
            buses = buses.filter(Tags__in = [tag])

        #if route and route != "-":
        #    buses = buses.filter(route=route)

        if company and company != "-":
            buses = buses.filter(bus_company=company)



    #products = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(buses, 8)
    try:
        buses = paginator.page(page)
    except PageNotAnInteger:
        buses = paginator.page(1)
    except EmptyPage:
        buses = paginator.page(paginator.num_pages)


    context = {
        #'routes':routes,
        'title':'list of Buses',
        'buses' : buses,
        'companies' : companies,
        'rating' : Bus.RATING_CHOICE,
        'tags' : Tag.objects.all()
    }

    count_hit = True
    


    return render(request, 'booking/index1.html', context)



@login_required
def like_pro(request):
    user = request.user
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        pro_obj = Bus.objects.get(id=bus_id)

        if user in pro_obj.liked.all():
            pro_obj.liked.remove(user)
        else:
            pro_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, bus_id=bus_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    #return redirect('post-list')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def like_company(request):
    user = request.user
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        pro_obj = Company.objects.get(id=bus_id)

        if user in pro_obj.cliked.all():
            pro_obj.cliked.remove(user)
        else:
            pro_obj.cliked.add(user)

        like, created = Like.objects.get_or_create(user=user, bus_id=bus_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    #return redirect('post-list')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_bus(request, bus_id, bus_slug):
    bus = get_object_or_404(Bus, id=bus_id,slug=bus_slug,available=True)
    #ins = Bus.objects.get(pk=bus_id)
    # first get the related HitCount object for your model object
    hit_count = HitCount.objects.get_for_object(bus)

    # next, you can attempt to count a hit and get the response
    # you need to pass it the request object as well
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    ##
    seats = Seatsall.objects.filter(seatbus=bus, available=True)
    #print(seats)



    #form = CartForm(instance=ins)
    if request.method == 'POST':
        form = CartForm(request, request.POST)#, instance=ins)
        if form.is_valid():
            data = request.POST.getlist('seatd')
            data = list(filter(None, data))
            print('data:',data)
            request.form_data = form.cleaned_data
            #data = request.form_data['seatd']
            data1 = request.form_data['quantity']
            #print('length', len(data), data)
            #print('quantity',data1)
            if len(data) != data1:
                form = CartForm(request, initial={'bus_id': bus.id})
                return render(request, 'booking/bus_detail.html', {'bus': bus,'form': form,'hit_count_response':hit_count_response,'message':'Quantity and Seats do not match','data': len(data),'data1':data1, 'seats':seats})

            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'bus_id': bus.id})
    return render(request, 'booking/bus_detail.html', {'bus': bus,'form': form,'hit_count_response':hit_count_response, 'seats':seats})





#ins = ClassName.objects.get(pk=pk)

#    form = ClassNameForm(instance=ins)
#    if request.method == 'POST':
#        form = form (request.POST, instance=ins)
#        if form.is_valid():
#            form.save()


#class ProDetailView(HitCountDetailView):
#    model = Product        
#    count_hit = True    
#    template = 'ecommerce_app/product_detail.html'

#    def get(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        context = self.get_context_data(object=self.object)
#        return redirect(self.object.product.image.url)



@login_required
def show_cart(request):

    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'booking/cart.html', {'cart_items': cart_items,'cart_subtotal': cart_subtotal})


@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o = Order(
                name = cleaned_data.get('name'),
                email = cleaned_data.get('email'),
                postal_code = cleaned_data.get('postal_code'),
                address = cleaned_data.get('address'),
            )
            o.user = request.user
            o.save()

            all_items = cart.get_all_cart_items(request)
            for cart_item in all_items:
                li = LineItem(
                    user_id = o.user.id,
                    bus_id = cart_item.bus_id,
                    price = cart_item.price,
                    quantity = cart_item.quantity,
                    order_id = o.id
                )

                li.save()

            cart.clear(request)

            request.session['order_id'] = o.id

            #messages.add_message(request, messages.INFO, 'Order Placed!')
            #return redirect('checkout')
            return redirect('process_payment')


    else:
        form = CheckoutForm()
        #return render(request, 'ecommerce_app/checkout.html', {'form': form})
        return render(request, 'booking/checkout.html', locals())



@login_required
def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost().quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'booking/process_payment.html', {'order': order, 'form': form})


@login_required
@csrf_exempt
def payment_done(request):
    return render(request, 'booking/payment_done.html')


@login_required
@csrf_exempt
def payment_canceled(request):
    return render(request, 'booking/payment_cancelled.html')
