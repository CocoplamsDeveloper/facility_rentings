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
    path('units/update', views.update_property_units),
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

    # path('token/get', oauth2.testing_tokens),
    # path('token/test', oauth2.with_decorator)
]

