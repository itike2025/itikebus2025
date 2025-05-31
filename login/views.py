from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegForm,UserUpdateForm,ProfileUpdateForm, ContactForm
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic 
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
#from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from django.views.generic import View
from web.models import Bus
from booking.models import  LineItem



# Create your views here.
def register(request):
    if request.method== 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your rwandabus account.'
            message = render_to_string('login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
            to_email = form.cleaned_data.get('email')
            #email = EmailMessage(mail_subject, message, to=[to_email])
            #email.send()
            user.email_user(mail_subject, message)
            #return HttpResponse('Please confirm your email addressto complete the registration')
            messages.success(request,f'Please confirm your email address to complete the registration')
            return redirect('login')

            #username = form.cleaned_data.get('username')
            #messages.success(request,f'User {username} created successfully!You can login')
            #return redirect('login')
    else:
        form = UserRegForm()
    return render(request,'login/register.html',{'form':form})




class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')



#@login_required
#def home_user(request):
    #return render(request, 'login/home_user.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been update Successfully!!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    
    context ={"u_form":u_form,"p_form":p_form,}
    return render(request,'login/profile.html',context)




def emailUs(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            enter_your_email = form.cleaned_data['enter_your_email']
            email = form.cleaned_data.get('email')
            #email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(enter_your_email, message, email, ['infoitike@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            username = form.cleaned_data.get('username')
            messages.success(request,f' Message sent successfully!')
            return redirect('emailus')
    return render(request, "login/contact_us.html", {'form': form})


def abouthabayeiki(request):
    return render(request, 'login/about_us.html')






#@login_required
#class DetailsView(generic.DetailView):
    #model = Ourservices

@login_required
def deleteuser(request,pk):
    if request.method == 'POST':
        try:
            u = User.objects.get(id=pk)
            #u.delete()
            u.is_active = False
            u.save()
            messages.success(request,f'User  successfully deactivated!') 
            return redirect('mainhome')
        except User.DoesNotExist:
            messages.error(request,f'User does not exist.')
            return render(request,'login/confirmdelete.html')
    else:
        return render(request,'login/confirmdelete.html')
    



@login_required
def home_user(request):
    os = LineItem.objects.filter(user=request.user ).order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(os, 5)
    try:
        os = paginator.page(page)
    except PageNotAnInteger:
        os = paginator.page(1)
    except EmptyPage:
        os = paginator.page(paginator.num_pages)
    return render(request, "login/home_user.html", {'os': os,})

