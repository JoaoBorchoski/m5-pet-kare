from django.urls import path
from . import views

urlpatterns = [
    path("groups/", views.GroupView.as_view()),
    path("groups/details/", views.GroupViewDetail.as_view()),
]
