from django.conf import settings
from django.core.mail import send_mail
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


class ArticleCreateView(CreateView):
    model = Article
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_detail")

    def get_success_url(self):
        return reverse_lazy("blog:article_detail", kwargs={"pk": self.object.pk})


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:article_list")