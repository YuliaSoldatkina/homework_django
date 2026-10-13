from django.urls import path

from catalog import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product_create/", views.ProductCreateView.as_view(), name="product_create"),
]