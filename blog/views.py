from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from taggit.models import Tag

from .forms import PostForm
from .models import Post


def about_page_view(request):
    return render(request, "about-page.html")


def home_page_view(request):
    return render(request, "home.html")


@permission_required("blog.add_blog")
def post_create_view(request):

    if request.method == "POST":
        new_post_form = PostForm(request.POST)
        if new_post_form.is_valid():
            tagslist = new_post_form.cleaned_data["tags"]
            new_post = new_post_form.save(commit=False)
            user = get_user_model()
            new_post.author = user.objects.get(username=request.user.username)
            new_post.tags.add(*tagslist)
            new_post.save()
            return redirect("post_list")
    else:
        new_post_form = PostForm()
    return TemplateResponse(request, "blog/post_form.html", {"form": new_post_form})


def post_list_view(request):

    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return TemplateResponse(
        request, "blog/post_list.html", {"post_list": posts, "page_obj": page_obj}
    )


def post_list_view_by_tag(request, tag_slug: str):

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug.lower())
        posts = Post.objects.all().order_by("-created").filter(tags__in=[tag])
    else:
        posts = Post.objects.all().order_by("-created")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return TemplateResponse(
        request,
        "blog/post_list.html",
        {"post_list": posts, "page_obj": page_obj, "tag": tag_slug},
    )


def post_detail_view(request, pk: int):

    post = get_object_or_404(Post, id=pk)

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=pk)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-created"
    )[:2]

    return TemplateResponse(
        request, "blog/post_detail.html", {"post": post, "similar_posts": similar_posts}
    )


@permission_required("blog.change_blog")
def post_update_view(request, pk: int):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        new_post_form = PostForm(request.POST, instance=post)
        if new_post_form.is_valid():
            tagslist = new_post_form.cleaned_data["tags"]
            new_post = new_post_form.save(commit=False)
            user = get_user_model()
            new_post.author = user.objects.get(username=request.user.username)
            new_post.tags.set(*tagslist)
            new_post.save()
            return redirect("post_list")
    else:
        new_post_form = PostForm(instance=post)
    return TemplateResponse(
        request, "blog/post_form.html", {"form": new_post_form, "post": post}
    )


# class HomeView(TemplateView):
#     template_name = "home.html"

# class AboutView(TemplateView):
#     template_name = "about-page.html"

# class PostListView(ListView):
#     model = Post
#     context_object_name = "post_list"
#     paginate_by = 5
#
#     def get_queryset(self, slug=None):
#         qs = self.model.objects.all().order_by("-created")
#         tag = self.kwargs.get("tag_slug")
#         if tag:
#             tag_slug = get_object_or_404(Tag, slug=tag.lower())
#             qs = qs.filter(tags__in=[tag_slug])
#         return qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tag"] = self.kwargs.get("tag_slug")
#         return context

# class PostDetailView(DetailView):
#     model = Post
#     context_object_name = "post"
#
#     def get_context_data(
#         self, **kwargs,
#     ):
#         post_tags_ids = self.object.tags.values_list("id", flat=True)
#         similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(
#             id=self.object.id
#         )
#         similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
#             "-same_tags", "-created"
#         )[:2]
#         context = super().get_context_data(**kwargs)
#         context["similar_posts"] = similar_posts
#         return context

# class PostCreateView(PermissionRequiredMixin, CreateView):
#     model = Post
#     permission_required = ("posts.add_post",)
#     fields = ["title", "content", "tags"]
#     # success_message = "Blog Post Successfully Created!"
#     context_object_name = "post"
#
#     def form_valid(self, form):
#         form.instance.author_id = self.request.user.id
#         super(PostCreateView, self).form_valid(form)
#         return HttpResponseRedirect(self.get_success_url())
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context["nav"] = "blog"

# class PostUpdateView(PermissionRequiredMixin, UpdateView):
#     model = Post
#     fields = ["title", "content", "tags"]
#     # success_message = "Blog Post Successfully Updated!"
#     permission_required = "posts.update_post"
