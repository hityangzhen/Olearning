from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('olearning.views',
    # Examples:
    url(r'^$',direct_to_template,{'template':'login.html'}),
    url(r'^index/$',direct_to_template,{'template':'login.html'}),
    url(r'^login/$','login'),
    url(r'^logout/$','logout'),
    url(r'^teacher/$',direct_to_template,{'template':'main/teacher-main.html'}),
    url(r'^student/$',direct_to_template,{'template':'main/student-main.html'}),
    url(r'^findpwd/$',direct_to_template,{'template':'forgetpwd.html'}),
    url(r'^findpwd/get/$','findPwd'),
    url(r'^admin/', include('admin.urls')),
    url(r'^course/', include('course.urls')),
    url(r'^exam/', include('exam.urls')),
    url(r'^learn/', include('learn.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^help/', direct_to_template,{'template':'help.html'}),
    # url(r'^olearning/', include('olearning.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r"^media/(?P<path>.*)$", \
            "django.views.static.serve", \
            {"document_root": settings.MEDIA_ROOT,}),
)
