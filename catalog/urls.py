from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog.views import (
    CategoryViewSet,
    ProductViewSet,
    home,
    contacts,
    product_detail,
    ProductCreateView,
)

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)