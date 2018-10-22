"""dwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',TemplateView.as_view(template_name="login.html"), name="login"),
    path('register/',TemplateView.as_view(template_name="register.html"), name="register"),
    path('home/',TemplateView.as_view(template_name="home.html"), name="home"),    
    path('content/',TemplateView.as_view(template_name="contentpage.html"), name="content"),
    path('userprofile/',TemplateView.as_view(template_name="userprofile.html"), name="userprofile"),
    path('myprofile/',TemplateView.as_view(template_name="myprofile.html"), name="myprofile"),
    path('admin/', admin.site.urls),    
    path('auth/',include("auth.urls"),name="auth"),
    path('feedapi/',include("dweetfeed.urls"),name="feed"),
    path('dweetapi/',include("dweetfeed.dweets.urls"),name="dweets"),
    path('userapi/',include("userprofile.urls"),name="userprofiles"),
]

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    
    import debug_toolbar    
    urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ] 

    # Create our schema's view w/ the get_schema_view() helper method. Pass in the proper Renderers for swagger
    from rest_framework.documentation import include_docs_urls
    urlpatterns += [ 
                path('docs/', include_docs_urls(title='Dwitter')) 
            ]

