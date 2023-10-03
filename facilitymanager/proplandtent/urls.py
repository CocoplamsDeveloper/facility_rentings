from django.contrib import admin
from django.urls import path, include
from . import views
# from graphene_django.views import GraphQLView

urlpatterns = [
    # ...
    # path("graphql", GraphQLView.as_view(graphiql=True)),
    path("landlord/<int:id>", views.get_landlord),
    path("tenant/<int:id>", views.get_tenant),
    path("property/<int:id>", views.get_property),
    path("tenancy/<int:id>", views.get_tenancy),
    path("units/<int:id>", views.get_units),
    path("addrole/", views.add_roles),
    path("ld-login", views.landlord_login),
    path("ld-logout", views.landlord_logout),
    path('add', views.create_properties),
    path('users/create', views.create_users),
    path('landlord-prop/get', views.landlord_property_list),
    path('alllandlord/props', views.get_landlord_properties_data),
    path('units/add', views.add_units),
    path('units/csv-add', views.get_units_from_csv),
    path('property/update', views.update_properties),
    path('allunits/get', views.get_landlord_all_units),
    path('units/filter', views.get_filtered_units),
    path('units/update', views.update_property_units),
    path('unit/delete', views.delete_units),
    path('tenant/add', views.create_tenants),
    path('tenancy/data', views.get_tenant_contract_form_details),
    path('tenancy/units', views.get_property_units),
    path('tenancy-record/create', views.create_tenancy_record)
]

