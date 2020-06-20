from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Post
from taggit.models import Tag


class PostCreateView(PermissionRequiredMixin,CreateView):
    model = Post
    permission_required = ("posts.add_post",)
    fields = ["title", "content", "tags"]
    # success_message = "Blog Post Successfully Created!"
    context_object_name = "post"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        super(PostCreateView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["nav"] = "blog"

class PostListView(ListView):
    model = Post
    context_object_name = "post_list"

    def get_queryset(self ,slug=None):
        qs = self.model.objects.all()
        tag = self.kwargs.get('tag_slug')
        if tag:
            tag_slug = get_object_or_404(Tag, slug=tag.lower())
            qs = qs.filter(tags__in=[tag_slug])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs,):
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids) \
            .exclude(id=self.object.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                            .order_by('-same_tags', '-created')[:2]
        context = super().get_context_data(**kwargs)
        context['similar_posts'] = similar_posts
        return context

class PostUpdateView(PermissionRequiredMixin,UpdateView):
    model = Post
    fields = ["title", "content", "tags"]
    # success_message = "Blog Post Successfully Updated!"
    permission_required = "posts.update_post"