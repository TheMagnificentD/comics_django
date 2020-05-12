from django.shortcuts import render
from django.http import HttpResponse
from .models import Box, Comic
from .forms import CreateNewBox, CreateNewComic
from django.contrib.auth.decorators import login_required


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
            t = Box(name=n, sImg=m)
            t.save()

    else:
        print("Its not Valid")
        form = CreateNewBox()

    return render(response, "main/newbox.html", {"form": form})


@login_required
def boxes(response):
    boxes = Box.objects.all()  # pylint: disable=no-member
    all_boxes = []
    for box in boxes:
        all_boxes.append({"id": box.id, "name": box.name, "image": box.sImg})

    return render(response, "main/boxes.html", {"boxes": all_boxes})


@login_required
def new_comic(response):
    if response.method == "POST":
        form = CreateNewComic(response.POST, response.FILES)

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
            t = Comic(
                box=b,
                publisher=p,
                name=n,
                variant=v,
                number=num,
                date=d,
                condition=c,
                owned=o,
                sImg=m,
            )
            t.save()

    else:
        print("Its not Valid")
        form = CreateNewComic()

    return render(response, "main/newcomic.html", {"form": form})


@login_required
def comics(response, id):
    box = Box.objects.get(id=id)  # pylint: disable=no-member
    comics = box.comic_set.all()
    all_comics = []
    for comic in comics:
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
    return render(response, "main/comics.html", {"comics": all_comics})

    # collection = Box.objects.get(id=id)# pylint: disable=no-member
    # book = collection.comic_set.get(id=id)
    # return HttpResponse("<h1>%s</h1><br></br><p>%s" %(collection.name, book.name))
    # return render(response,'main/comics.html',{"box":collection, "comic":book})
