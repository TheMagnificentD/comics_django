from django.urls import path
from . import views

from LongestBox import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from register import views as rv


urlpatterns = [
    path("", views.home, name="home"),
    path("confirm_registration/", rv.conf_registration, name="confirm registration"),
    path("boxes/", views.boxes, name="boxes"),
    path("newbox/", views.new_box, name="new box"),
    path("deletebox/<int:id>", views.delete_box, name="delete box"),
    path("editbox/<int:id>", views.edit_box, name="edit box"),
    path("comics/<int:id>", views.comics, name="comics"),
    path("box/<int:id>/newcomic/", views.new_comic, name="new comic"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
