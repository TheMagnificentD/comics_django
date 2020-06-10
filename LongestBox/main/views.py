from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.forms import HiddenInput
from django.http import HttpResponse
from .models import Box, Comic
from .forms import BoxForm, ComicForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


def home(response):

    return render(response, "main/home.html", {})


@login_required
def boxes(response):
    boxes = get_list_or_404(Box, user=response.user.pk)

    return render(response, "main/boxes.html", {"boxes": boxes})


@login_required
def new_box(response):

    if response.method == "POST":
        form = BoxForm(response.POST, response.FILES)

        if form.is_valid():
            n = form.cleaned_data["name"]
            m = form.cleaned_data["sImg"]

            response.user.box_set.create(name=n, sImg=m)
            return HttpResponseRedirect(reverse("boxes"))

    else:
        form = BoxForm()

    return render(response, "main/newbox.html", {"form": form})


@login_required
def edit_box(response, slug):

    box = get_object_or_404(Box, slug=slug)
    box.slug = None
    if response.method == "POST":
        form = BoxForm(response.POST, response.FILES, instance=box)
        if form.is_valid():
            n = form.cleaned_data["name"]
            m = form.cleaned_data["sImg"]
            box.name = n
            box.sImg = m
            box.save()
            return HttpResponseRedirect(reverse("boxes"))

    else:
        form = BoxForm(instance=box)

    return render(response, "main/editbox.html", {"form": form, "box": box})


@login_required
def delete_box(response, slug):

    box = get_object_or_404(Box, slug=slug)
    box.delete()
    # messages.success(response, "Box has been deleted")
    return HttpResponseRedirect(reverse("boxes"))


@login_required
def comics(response, slug):

    box = get_object_or_404(Box, slug=slug)
    comics = get_list_or_404(Comic, user=response.user.pk)

    return render(response, "main/comics.html", {"comics": comics, "box": box})


@login_required
def new_comic(response, slug):

    box = get_object_or_404(Box, slug=slug)

    if response.method == "POST":
        form = ComicForm(response.POST, response.FILES)

        if form.is_valid():
            p = form.cleaned_data["publisher"]
            n = form.cleaned_data["name"]
            num = form.cleaned_data["number"]
            v = form.cleaned_data["variant"]
            d = form.cleaned_data["date"]
            c = form.cleaned_data["condition"]
            o = form.cleaned_data["owned"]
            m = form.cleaned_data["sImg"]

            response.user.comic_set.create(
                box=box,
                publisher=p,
                name=n,
                variant=v,
                number=num,
                date=d,
                condition=c,
                owned=o,
                sImg=m,
            )
            return HttpResponseRedirect("/boxes/%s" % box.slug)
        else:
            return render(response, "main/404.html", {})
    else:

        form = ComicForm(initial={"box": box.id})
        form.fields["box"].widget = HiddenInput()
        return render(response, "main/newcomic.html", {"form": form})


def edit_comic(response, slug, comic_slug):
    box = get_object_or_404(Box, slug=slug)
    comic = get_object_or_404(Comic, slug=comic_slug)
    comic.slug = None

    if response.method == "POST":
        form = ComicForm(response.POST, response.FILES, instance=comic)

        if form.is_valid():
            b = form.cleaned_data["box"]
            p = form.cleaned_data["publisher"]
            n = form.cleaned_data["name"]
            num = form.cleaned_data["number"]
            v = form.cleaned_data["variant"]
            d = form.cleaned_data["date"]
            c = form.cleaned_data["condition"]
            o = form.cleaned_data["owned"]
            m = form.cleaned_data["sImg"]

            comic.box = b
            comic.publisher = p
            comic.name = n
            comic.number = num
            comic.variant = v
            comic.date = d
            comic.condition = c
            comic.owned = o
            comic.sImg = m
            comic.save()
            return HttpResponseRedirect("/boxes/%s/" % box.slug)

    else:
        form = ComicForm(instance=comic)
        # This adjusts the queryset of the form= default=all() and now its filtered on user
        form.fields["box"].queryset = Box.objects.filter(user=response.user.pk)

    return render(
        response, "main/editcomic.html", {"form": form, "box": box, "comic": comic}
    )


@login_required
def delete_comic(response, slug, comic_slug):
    comic = get_object_or_404(Comic, slug=comic_slug)
    box = comic.box
    comic.delete()
    # messages.success(response, "Box has been deleted")
    return HttpResponseRedirect("/boxes/%s/" % box.slug)
