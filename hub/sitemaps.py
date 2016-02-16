from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from hub.models import Category, Job


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, item):
        return item.get_jobs_url()


class JobSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Job.objects.filter(status='ACTIVE', approved=True)


class StaticPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['page_about', 'page_faq', 'page_contact']

    def location(self, item):
        return reverse(item)

sitemaps = {'categories': CategorySitemap, 'jobs': JobSitemap, 'pages': StaticPageSitemap}
