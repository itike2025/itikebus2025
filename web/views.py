from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from . import forms
from .models import Bus,Company, Seatsall
import calendar
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from booking.models import  LineItem

 

 
def find_bus(request):
    form = forms.FormFindBus
        
    template = 'home.html'
    context = {'form': form}
    return render(request, template, context)


 
def select(request):

    #bus_type = request.GET.get('bus_type')
    ###qs = Bus.objects.filter(type_of_bus=bus_type)

    bus_from = request.GET.get('bus_from')
    ###qs = Bus.objects.filter(route__location_from=bus_from)
    
    bus_to = request.GET.get('bus_to')
    ####qs = qs.filter(route__location_to=bus_to)
    
    date_string = request.GET.get('date')
    
    request.session['bus_from'] = bus_from
    request.session['bus_to'] = bus_to
    request.session['date'] = date_string
    #request.session['time'] = time_string


    #qs = Bus.objects.filter(route__location_from=bus_from, route__location_to=bus_to, departure_date=date_string)

        
    #context = {'qs': qs,}
    #template = 'select.html'
    #return render(request, template, context)


    #print('bus_from',bus_from,'bus_to',bus_to,'date',date_string)

    if bus_from == bus_to:
        #raise forms.ValidationError("From and To are same")
        form = forms.FormFindBus()
        return render(request,'home.html',{'form':form, 'message':"From (aho uri) and To (aho ugiye) are same (ni hamwe)"})

    buses = Bus.objects.filter(location_from=bus_from, location_to=bus_to, departure_date=date_string)
    #products = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(buses, 4)
    try:
        buses = paginator.page(page)
    except PageNotAnInteger:
        buses = paginator.page(1)
    except EmptyPage:
        buses = paginator.page(paginator.num_pages)

    count_hit = True

    return render(request,'select.html', {'buses': buses,})




#class CompanyListView(ListView):
#    model = Company
#    template_name = 'company_home.html'
#    context_object_name = 'companies'
#    ordering = ['-created']
#    paginate_by = 5
    
#    def get_queryset(self):
#        order_by = self.kwargs.get('order_by') or '-created'
#        return Company.objects.order_by(order_by)


@login_required
def CompanyListView(request):
    companies = Company.objects.filter(available=True).order_by('-created')
    page = request.GET.get('page', 1)

    paginator = Paginator(companies, 4)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    count_hit = True
    return render(request,'company_home.html',{'companies':companies})


def alltickets(request):
    buses = Bus.objects.filter(available=True).order_by('-created')
    page = request.GET.get('page', 1)

    paginator = Paginator(buses, 4)
    try:
        buses = paginator.page(page)
    except PageNotAnInteger:
        buses = paginator.page(1)
    except EmptyPage:
        buses = paginator.page(paginator.num_pages)

    count_hit = True
    return render(request,'alltickets.html',{'buses':buses})




#class UserCompanyBusListView(ListView):
#    model = Bus
#    template_name = 'company_detail.html'
#    context_object_name = 'buses'


#    def get_queryset(self):
#        user = get_object_or_404(User, username= self.kwargs.get('username'))
#        company = get_object_or_404(Company, name= self.kwargs.get('manager'))
#        return Bus.objects.filter(bus_company = company).order_by('-created')
@login_required
def UserCompanyBusListView(request, pk):
    company = get_object_or_404(Company, id=pk,available=True)
    #ins = Bus.objects.get(pk=bus_id)
    # first get the related HitCount object for your model object
    hit_count = HitCount.objects.get_for_object(company)

    # next, you can attempt to count a hit and get the response
    # you need to pass it the request object as well
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    #buses = company.bus_set.all()
    buses = Bus.objects.filter(bus_company=company).order_by('-created')
    #print('bbbb..',buses)



    ##
    page = request.GET.get('page', 1)

    paginator = Paginator(buses, 4)
    try:
        buses = paginator.page(page)
    except PageNotAnInteger:
        buses = paginator.page(1)
    except EmptyPage:
        buses = paginator.page(paginator.num_pages)

    #count_hit = True
    context = {'company':company,'buses':buses,'hit_count':hit_count}
    return render(request,'company_detail.html',context)

#queryset = demo.objects.filter(name="non_existent_name")

#if queryset.exists():
#    serializer = DemoSerializer(queryset, many=True)
#    return Response(serializer.data)
#else:
#    return Response(status=status.HTTP_404_NOT_FOUND)


@login_required
def company_dashboard(request):
    co = Company.objects.filter(manager=request.user)
    return render(request, 'company_dashboard.html', {'co':co,})



@login_required
def company_create(request):
    exst = Company.objects.filter(manager=request.user)
    if request.method == "POST":
        form = forms.CompanyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.manager = request.user
            form.save()
            messages.success(request, f'Your company has been created Successfully!!')
            return redirect('web:company-home')
    else:
        form = forms.CompanyCreateForm()
    return render(request, 'company_form.html', {'form': form,'exst':exst,})

    

@login_required
def company_update(request,pk):
    if request.method == "POST":
        form = forms.CompanyUpdateForm(request.POST, request.FILES, instance= Company.objects.get(id=pk))
        if form.is_valid():
            form.instance.manager = request.user
            form.save()
            messages.success(request, f'Your company has been updated Successfully!!')
            return redirect('web:company-home')
    else:
        form = forms.CompanyUpdateForm(instance= Company.objects.get(id=pk))
    return render(request, 'company_update.html', {'form': form})


#class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#    model = Company
#    context_object_name = 'company' 
#    success_url = '/'

#    def test_func(self):
#        company = self.get_object()
#        if self.request.user == company.manager:
#            return True
#        return False

@login_required
def CompanyDeleteView(request,pk):
    if request.method == 'POST':
        try:
            company = Company.objects.get(id=pk)
            company.delete()
            #company.available = False
            #company.save()
            messages.success(request,f'Company  successfully deactivated!') 
            return redirect('/')
        except Company.DoesNotExist:
            messages.error(request,f'Company does not exist.')
            return render(request,'company_confirm_delete.html')
    else:
        return render(request,'company_confirm_delete.html')

@login_required
def company_bus_detail(request, pk, slug):
    bus = get_object_or_404(Bus, id=pk,slug=slug,available=True)
    #ins = Bus.objects.get(pk=bus_id)
    # first get the related HitCount object for your model object
    hit_count = HitCount.objects.get_for_object(bus)

    # next, you can attempt to count a hit and get the response
    # you need to pass it the request object as well
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    ##
    seats = Seatsall.objects.filter(seatbus=bus)
    orders = LineItem.objects.filter(bus=bus)

    return render(request, 'company_bus_detail.html', {'bus': bus,'hit_count_response':hit_count_response, 'seats':seats,'orders':orders})

@login_required
def bus_create(request):
    if request.method == "POST":
        form = forms.BusCreateForm(request.POST, request.FILES)
        if form.is_valid():
            #form.instance.bus_company.manager = request.user
            form.instance.bus_company = request.user.company
            #print('bc',form.instance.bus_company,':',request.user.company)
            form.save()
            messages.success(request,f'Bus  successfully created!') 
            return redirect('web:company-home')
    else:
        form = forms.BusCreateForm()
    return render(request, 'bus_form.html', {'form': form})

@login_required
def bus_update(request,pk):
    if request.method == "POST":
        form = forms.BusUpdateForm(request.POST, request.FILES, instance= Bus.objects.get(id=pk))
        if form.is_valid():
            form.instance.bus_company.manager = request.user
            form.save()
            messages.success(request,f'Bus  successfully Updated!') 
            return redirect('web:company-home')
    else:
        form = forms.BusUpdateForm(instance= Bus.objects.get(id=pk))
    return render(request, 'bus_form.html', {'form': form})




@login_required
def BusDeleteView(request,pk):
    if request.method == 'POST':
        try:
            bus = Bus.objects.get(id=pk)
            bus.delete()
            #company.available = False
            #company.save()
            messages.success(request,f'Bus  successfully deactivated!') 
            return redirect('web:company-home')
        except Company.DoesNotExist:
            messages.error(request,f'bus does not exist.')
            return render(request,'bus_confirm_delete.html')
    else:
        return render(request,'bus_confirm_delete.html')


#class BusDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#    model = Bus
#    context_object_name = 'bus' 
#    success_url = '/'

#    def test_func(self):
#        bus = self.get_object()
#        if self.request.user == bus.bus_company.manager:
#            return True
#        return False