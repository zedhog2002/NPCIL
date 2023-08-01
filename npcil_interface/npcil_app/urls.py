from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('package/<int:pk>', views.package_record, name='package'),
    path('delete_package/<int:pk>', views.delete_package_record, name='delete_package'),
    path('add_package/', views.add_package_record, name='add_package'),
    path('update_package/<int:pk>', views.update_package_record, name='update_package'),
    path('show_package/', views.show_package_record, name='show_package')
]
