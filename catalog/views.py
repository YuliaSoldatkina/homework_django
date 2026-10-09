from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


def home(request):
    products = Product.objects.all()

    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "catalog/home.html", context)


def contacts(request):
    return render(request, "catalog/contacts.html")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "image", "category", "price"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")