from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        if product.owner != self.request.user:
            raise PermissionDenied

        return product


@method_decorator(login_required, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm("catalog.delete_product")

        if not is_owner and not is_moderator:
            raise PermissionDenied

        return product


@method_decorator(login_required, name="dispatch")
class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = []
    http_method_names = ["post"]
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_published = False
        product.save()
        return redirect(reverse("home"))


@method_decorator(login_required, name="dispatch")
class ProductPublishView(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = []
    http_method_names = ["post"]
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_published = True
        product.save()
        return redirect(reverse("home"))


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
