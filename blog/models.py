import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class DraftPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(draft=True).order_by("-created")


class LivePostsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(draft=False, portfolio=False)
            .order_by("-created")
        )


class PortfolioPostsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(draft=False, portfolio=True)
            .order_by("-created")
        )


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=400, null=True)
    draft = models.BooleanField(default=True)
    portfolio = models.BooleanField(default=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=UUIDTaggedItem)
    slug = models.SlugField(null=True)
    objects = models.Manager()
    live_posts = LivePostsManager()
    draft_posts = DraftPostsManager()
    portfolio_posts = PortfolioPostsManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_tag_ids(self):
        return self.tags.values_list("id", flat=True)
