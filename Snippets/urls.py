"""Snippets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from MainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index_page, name='home'),
                  path('snippets/add', views.add_snippet_page, name='snippets-add'),
                  path('snippets/list', views.snippets_page, name='snippets-list'),
                  path('snippets/<int:snippet_number>', views.show_snippet, name='show-snippet'),
                  path('create_new_snippet', views.create_new_snippet, name='create_new_snippet'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
