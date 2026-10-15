"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sankster import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('bartender-dashboard/', views.barista_dashboard, name='barista_dashboard'),
    path('server-dashboard/', views.server_dashboard, name='server_dashboard'),

    path('manage-menu/', views.manage_menu, name='manage_menu'),
    path('manage-menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('manage-menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),

    path('create-order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/order-detail', views.order_detail, name='order_detail'),

    path('manage-staff/', views.manage_staff, name = 'manage_staff' ),
    path('manage-staff/create_worker/', views.create_worker, name='create_worker'),
    path('edit-worker/<int:worker_id>/', views.edit_worker, name='edit_worker'),

    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('get-order-status/', views.get_order_status, name='get_order_status'),
    path('mark-order-delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),

    path('call-server/', views.call_server, name='call_server'),

    path('mark-order-received/<int:order_id>/', views.mark_order_received, name='mark_order_received'),
]
