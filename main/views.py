from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from .forms import AddUrlForm
from .models import PageText, PageUrl


def home(request, tpl="main/home.html"):
    urls = PageUrl.objects.all()[:10]
    return render(request, tpl, {"urls": urls})


def view(request, tpl="main/view.html"):
    page_url = get_object_or_404(PageUrl, url=request.GET.get("url"))
    ctx = {"texts": page_url.texts.order_by("-created_on").all()}
    return render(request, tpl, ctx)


def diff(request, tpl="main/diff.html"):
    t1 = PageText.objects.filter(text_hashed=request.GET.get("v")).first()
    t2 = PageText.objects.filter(url=t1.url)
    t2 = t2.filter(created_on__gt=t1.created_on)
    t2 = t2.exclude(text_hashed=t1.text_hashed)
    t2 = t2.first()
    return render(request, tpl, {"text1": t1, "text2": t2})


def delete(request, tpl="main/del.html"):
    if request.method == "POST":
        PageUrl.objects.get(pk=request.POST["pk"]).delete()
        return HttpResponseRedirect("/")
    return HttpResponseNotFound()


def add(request, tpl="main/add.html"):
    if request.method == "POST":
        form = AddUrlForm(request.POST)
        if form.is_valid():
            page_url = PageUrl(url=form.cleaned_data["url"])
            page_url.save()
            return HttpResponseRedirect("/")
    form = AddUrlForm()
    return render(request, tpl, {"form": form})
