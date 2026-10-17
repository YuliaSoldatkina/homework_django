from django.urls import path

from catalog import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product_create/", views.ProductCreateView.as_view(), name="product_create"),
    path("product_update/<int:pk>/", views.ProductUpdateView.as_view(), name="product_update"),
    path("product_delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product_delete"),
]