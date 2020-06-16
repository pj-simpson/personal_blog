from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from blog.models import Post




class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content"]
    # success_message = "Blog Post Successfully Created!"
    permission_required = "posts.add_post"
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

class PostDetailView(DetailView):
    model = Post

class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "content"]
    # success_message = "Blog Post Successfully Updated!"
    permission_required = "posts.update_post"