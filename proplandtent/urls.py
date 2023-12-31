from django.contrib import admin
from django.urls import path, include
from . import views, oauth2
# from graphene_django.views import GraphQLView

urlpatterns = [
    # ...
    # path("graphql", GraphQLView.as_view(graphiql=True)),
    # path("landlord/<int:id>", views.get_landlord),
    path("tenant/<int:id>", views.get_tenant),
    path("property/<int:id>", views.get_property),
    path("tenancy/<int:id>", views.get_tenancy),
    path("units/<int:id>", views.get_units),
    path("landlord/<int:id>", views.get_landlord),
    path("floors/units", views.get_unit_floor_wise),
    path("addrole/", views.add_roles),
    path("user/logout", views.user_logout),
    path('add', views.create_properties),
    path('property-details/add', views.add_property_additional_details),
    path('users/create', views.create_users),
    path('landlord-prop/get', views.landlord_property_list),
    path('alllandlord/props', views.get_landlord_properties_data),
    path('units/add', views.add_units),
    path('property/delete', views.soft_delete_property),
    path('units/csv-add', views.get_units_from_csv),
    path('property/update', views.update_properties),
    path('allunits/get', views.get_landlord_all_units),
    path('units/filter', views.get_filtered_units),
    path('units/update', views.update_units),
    path('unit/delete', views.delete_units),
    path('tenancy/data', views.get_tenant_contract_form_details),
    path('tenancy/units', views.get_property_units),
    path('tenancy-record/create', views.create_tenancy_record),
    path('details/tenants', views.get_tenants_data),
    path('tenants/update', views.update_tenants_details),
    path('tenant-docs/get', views.get_tenants_documents),
    path('contract-doc/update', views.update_tenancy_document),
    path('contract-status/update', views.update_tenancy_status),
    path('user/login', views.user_login),
    path('contract-doc/download', views.serve_contract_document),
    path('login/refresh', views.refresh_user_login),
    path('', views.health_check_api),
    path('property/search', views.search_properties),
    path('unit/search', views.search_units),
    path('tenant/search', views.search_tenants),
    path('tenants/filter', views.filter_tenants),
    path('landlord/create', views.create_landlords),
    path('landlords/get', views.get_landlords_details),
    path('landlord-page/stats', views.get_landlord_page_statistics),
    path('landlord/update', views.update_landlord),
    path('landlord/docs', views.get_landlord_documents),
    path('document/add', views.add_document),
    path('document/download', views.download_document),
    path('facility/add', views.add_facility),
    path('facility/get', views.get_facilities),
    # path('prop-del', views.del_props),
    path('property/docs', views.property_documents),
    path('prop-doc/add', views.add_property_document),
    path('prop-doc/download', views.download_property_document),
    path('property/stats', views.get_property_page_statistics),
    path('unit/stats', views.get_units_page_statistics),
    path('unitcsvsample/download', views.serve_sample_unit_csv),
    path('tenant/create', views.create_tenants),
    path('required-doc/create', views.add_tenant_required_docs),
    path('required-doc/get', views.get_tenant_required_docs)



    # path('token/get', oauth2.testing_tokens),
    # path('token/test', oauth2.with_decorator)
]

