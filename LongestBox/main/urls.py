from django.urls import path
from . import views

from LongestBox import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from register import views as rv


urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # Register
    path("confirm_registration/", rv.conf_registration, name="confirm registration"),
    # Boxes
    path("boxes/", views.boxes, name="boxes"),
    path("boxes/new-box/", views.new_box, name="new box"),
    path("boxes/<str:slug>/edit-box", views.edit_box, name="edit box"),
    path("boxes/<str:slug>/delete-box", views.delete_box, name="delete box"),
    # Comics
    path("boxes/<str:slug>/", views.comics, name="comics"),
    path("boxes/<str:slug>/new-comic", views.new_comic, name="new comic"),
    path(
        "boxes/<str:slug>/<str:comic_slug>/edit-comic",
        views.edit_comic,
        name="edit comic",
    ),
    path(
        "boxes/<str:slug>/<str:comic_slug>/delete-comic",
        views.delete_comic,
        name="delete comic",
    ),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
