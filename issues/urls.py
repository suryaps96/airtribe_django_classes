from django.urls import path

from . import views
urlpatterns = [
    path('hello/',views.hello_world),
    path('reporter/',views.reporter),
    path('issue/',views.issue)
]