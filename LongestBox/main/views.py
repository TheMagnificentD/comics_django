from django.shortcuts import render
from django.forms import HiddenInput
from django.http import HttpResponse
from .models import Box, Comic
from .forms import CreateNewBox, CreateNewComic
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.


def home(response):
    return render(response, "main/home.html", {})


@login_required
def new_box(response):
    if response.method == "POST":
        form = CreateNewBox(response.POST, response.FILES)

        if form.is_valid():
            n = form.cleaned_data["name"]
            m = form.cleaned_data["sImg"]
        
            response.user.box_set.create(name=n, sImg=m)
            return HttpResponseRedirect(reverse('boxes'))

    else:
        print("Its not Valid")
        form = CreateNewBox()

    return render(response, "main/newbox.html", {"form": form})


@login_required
def boxes(response):
    boxes = Box.objects.all()  # pylint: disable=no-member
    all_boxes = []
    for box in boxes:
        if box.user_id == response.user.pk:
            all_boxes.append({"id": box.id, "name": box.name, "image": box.sImg})

    return render(response, "main/boxes.html", {"boxes": all_boxes})


@login_required
def new_comic(response, id):
    if response.method == "POST":
        form = CreateNewComic(response.POST, response.FILES, initial={'box': id})

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
            
            response.user.comic_set.create(box=b, publisher=p, name=n,
            variant=v, number=num, date=d, condition=c, owned=o, sImg=m)
            return HttpResponseRedirect('/comics/%s' % int(b.pk))
    else:
        url = response.get_raw_uri()
        box_id = int(url.split('/')[4])
        form = CreateNewComic(initial={'box': box_id})
        form.fields['box'].widget = HiddenInput()
        return render(response, "main/newcomic.html", {"form": form})


@login_required
def comics(response, id):
    box = Box.objects.get(id=id)  # pylint: disable=no-member
    comics = box.comics.all()
    all_comics = []
    for comic in comics:
        if comic.user_id == response.user.pk:
            all_comics.append(
                {
                    "image": comic.sImg,
                    "publisher": comic.publisher,
                    "id": comic.id,
                    "name": comic.name,
                    "number": comic.number,
                    "variant": comic.variant,
                    "condition": comic.condition,
                    "date": comic.date,
                    "owned": comic.owned,
                }
            )
    return render(response, "main/comics.html", {"comics": all_comics, "box": box.pk})

    # collection = Box.objects.get(id=id)# pylint: disable=no-member
    # book = collection.comic_set.get(id=id)
    # return HttpResponse("<h1>%s</h1><br></br><p>%s" %(collection.name, book.name))
    # return render(response,'main/comics.html',{"box":collection, "comic":book})
