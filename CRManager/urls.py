"""CRManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from user.views import CustomAuthToken, UserProfileView

from manager.views import ProcessView, CRView


urlpatterns = [
    # Process URLs
    path('process/', ProcessView.as_view()),
    path('process/<int:pk>/', ProcessView.as_view()),

    # CR URLs
    path('cr/', CRView.as_view()),
    path('cr/<int:pk>/', CRView.as_view()),

    # User Profile URLs
    path('user_profile/', UserProfileView.as_view()),
    path('user_profile/<int:pk>/', UserProfileView.as_view()),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', CustomAuthToken.as_view())
]
