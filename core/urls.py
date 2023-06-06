from django.urls import path
from . import views
urlpatterns = [
    path("v1/register/", views.register, name="register"),
    path("v1/login/", views.login, name="login"),
    path("v1/refresh-token/", views.refresh_token, name="refresh-token"),
    path("v1/snippet-detail/<int:pk>/",
         views.snippet_detail, name="snippet-detail"),
    path("v1/snippet-list/", views.snippet_list, name="snippet_list"),
    path("v1/snippet-create/", views.snippet_create, name="snippet_create"),
    path("v1/snippet-update/<int:pk>/", views.snippet_update, name="snippet_update"),
    path("v1/delete-snippets/", views.delete_snippets, name="delete_snippets"),
    path("v1/tag-list/", views.UserList.as_view(), name="list-tag"),
    path("v1/tag-deatils/<int:pk>/", views.tag_details, name="tag-details"),
]
