from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.all()


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "image", "category", "price"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer