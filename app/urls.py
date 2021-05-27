from django.urls import path

from .views import upload, query_top

urlpatterns = [
    path('upload/', upload),
    path('query_top/', query_top)
]
