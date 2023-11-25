from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class PublishedManager(models.Manager):
    """Manager for published posts

    Args:
        models (): mother class
    """

    def get_queryset(self):
        """returns all published posts"""
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PD", "Published"

    # creating managers' instances
    objects = models.Manager()
    published = PublishedManager()

    # Database fields
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    body = models.TextField()
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    # Metadata defines in which order will we get elements
    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def get_absolute_url(self) -> str:
        return reverse(
            "blog:post_detail",
            args=[self.id],  # type: ignore
        )

    def __str__(self) -> str:
        return self.title
