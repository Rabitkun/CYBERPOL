from django.urls import path, re_path

from . import views
from . import rest

#views
urlpatterns = [
    #path('auth/', authentication, name='authentication'),
    #path('vm_list/', views.vm_list, name='vm_list'),

]

#rest
urlpatterns += [
    path('create_vm_by_ref_rest/', rest.create_vm_by_ref, name='create_vm_by_ref_rest'),
    path('delete_vm_rest/', rest.delete_vm, name='delete_vm_rest'),
    path('get_vms_list_rest/', rest.get_vms_list, name='get_vms_list_rest'),
]