from django.urls import path, re_path

from . import views
from . import rest

#views
urlpatterns = [
    #path('auth/', authentication, name='authentication'),
    #path('vm_list/', views.vm_list, name='vm_list'),
    path('lab_field/', views.lab_field, name='lab_field'),
]

#rest
urlpatterns += [
    path('create_vm_by_ref_rest/', rest.create_vm_by_ref, name='create_vm_by_ref_rest'),
    path('delete_vm_rest/', rest.delete_vm, name='delete_vm_rest'),
    path('get_vms_list_rest/', rest.get_vms_list, name='get_vms_list_rest'),
    path('get_vms_status_rest/', rest.get_vm_status, name='get_vms_status_rest'),
    path('start_vm_rest/', rest.start_vm, name='start_vm_rest'),
    path('shutdown_vm_rest/', rest.shutdown_vm, name='shutdown_vm_rest'),
    path('forceoff_vm_rest/', rest.forceoff_vm, name='forceoff_vm_rest'),
    path('set_vnc_port_vm_rest/', rest.set_vnc_port_vm, name='set_vnc_port_vm_rest'),
    path('create_cloud_node_rest/', rest.create_cloud_node, name='create_cloud_node_rest'),
    path('remove_cloud_node_rest/', rest.remove_cloud_node, name='remove_cloud_node_rest'),
    path('get_node_info_rest/', rest.get_node_params, name='get_node_info_rest'),
]