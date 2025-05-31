from django.urls import path
from . import views


urlpatterns = [
    #path('categories/', views.cindex, name='cindex'),
    #path('<slug:category_slug>/',views.cindex,name='product_list_by_category'),
    path('', views.index, name='index'),
    path('search/', views.index1, name='index1'),
    path('booking/<int:bus_id>/<slug:bus_slug>/',views.show_bus, name='bus_detail'),
    path('cart/', views.show_cart, name='show_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('like/', views.like_pro, name='like-pro'),
    path('likec/', views.like_company, name='like-company'),

]

