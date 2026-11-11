from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            send_mail(
                subject="Поздравляем: статья достигла 100 просмотров!",
                message=(
                    f"Статья «{self.object.title}» достигла 100 просмотров."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

        return self.object


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")
    permission_required = "blog.add_article"


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/article_form.html"
    permission_required = "blog.change_article"

    def get_success_url(self):
        return reverse_lazy("blog:article_detail", kwargs={"pk": self.object.pk})


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:article_list")
    permission_required = "blog.delete_article"


class ArticlePublishView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = []
    http_method_names = ["post"]
    permission_required = "blog.can_publish_article"

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        article.is_published = True
        article.save()
        return redirect(reverse("blog:article_list"))


class ArticleUnpublishView(PermissionRequiredMixin, UpdateView):
    model = Article
    fields = []
    http_method_names = ["post"]
    permission_required = "blog.can_publish_article"

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        article.is_published = False
        article.save()
        return redirect(reverse("blog:article_list"))
