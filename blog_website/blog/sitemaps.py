from django.contrib.sitemaps import Sitemap
from .models import Post, PublishedManager

class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self) -> PublishedManager:
        return Post.published.all()
    
    def lastmod(self, obj: PublishedManager) -> PublishedManager:
        return obj.updated  # type: ignore