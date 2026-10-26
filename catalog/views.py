from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from catalog.forms import ProductForm
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


@method_decorator(login_required, name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


@method_decorator(login_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")


@method_decorator(login_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")


@method_decorator(login_required, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CategorySerializer if False else ProductSerializer
