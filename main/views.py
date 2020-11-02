from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from .forms import AddUrlForm
from .models import PageUrl


def home(request, tpl="main/home.html"):
    urls = PageUrl.objects.all()[:10]

    return render(request, tpl, {"urls": urls})


def view(request, tpl="main/view.html"):
    page_url = get_object_or_404(PageUrl, url=request.GET.get("url"))
    return render(request, tpl, {"texts": page_url.texts.order_by("-created_on").all()})


def delete(request, tpl="main/del.html"):
    if request.method == 'POST':
        PageUrl.objects.get(pk=request.POST["pk"]).delete()
        return HttpResponseRedirect('/')
    return HttpResponseNotFound()


def add(request, tpl="main/add.html"):
    if request.method == 'POST':
        form = AddUrlForm(request.POST)
        if form.is_valid():
            page_url = PageUrl(url=form.cleaned_data["url"])
            page_url.save()
            return HttpResponseRedirect('/')

    form = AddUrlForm()
    return render(request, tpl, {'form': form})
