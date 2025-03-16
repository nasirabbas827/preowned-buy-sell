from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('order/<int:product_id>/', views.make_order, name='make_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('payment_success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
    path('report-product/<int:product_id>/', views.report_product, name='report_product'),
    path('order-transactions/<int:order_id>/', views.order_transactions, name='order_transactions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
