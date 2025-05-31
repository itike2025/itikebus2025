#from django.conf.urls import url
from django.urls import path
from .import views

app_name = 'web'
urlpatterns = [
    #path('', views.find_bus, name='home'), 
    #url(r'^select/', views.select, name='select'),
    path('findbus/',views.find_bus, name='findbus'),
    path('select/',views.select, name='select'),
    path('allt/',views.alltickets, name='all-tickets'),
    path('company/', views.CompanyListView, name='company-home'),
    path('company/<str:order_by>', views.CompanyListView, name='company-home'),
    path('company/<int:pk>/', views.UserCompanyBusListView, name='company-detail'),
    path('company/dashboard/', views.company_dashboard, name='company-dashboard'),
 	#path('user/dashboard/<str:username>', UserDashboard.as_view(), name='user-dashboard'),
 	path('company/add/',views.company_create, name='company-create'),
    path('<int:pk>/update_company/', views.company_update, name='company-update'),
    path('<int:pk>/delete_company/', views.CompanyDeleteView, name='company-delete'),

    path('bus/add/',views.bus_create, name='bus-create'),
    path('bus/<int:pk>/<str:slug>/',views.company_bus_detail, name='company-bus-detail'),
    path('<int:pk>/update_bus/', views.bus_update, name='bus-update'),
    path('<int:pk>/delete_bus/', views.BusDeleteView, name='bus-delete'),
]