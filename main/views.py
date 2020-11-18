import difflib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import AddUrlForm
from .models import PageText, PageUrl


def home(request, tpl="main/home.html"):
    q = request.GET.get("q")
    query = PageUrl.objects
    if q:
        query = query.filter(url__contains=str(q))
    urls = query.order_by("-created_on").all()[:100]
    return render(request, tpl, {"urls": urls, "form": AddUrlForm()})


def view(request, tpl="main/view.html"):
    url = get_object_or_404(PageUrl, url=request.GET.get("url"))
    texts =  PageText.objects.filter(url=url).order_by("-pk")
    for i, x in enumerate(list(texts)[:-1]):
        setattr(x, "prev_text_hashed", texts[i+1].text_hashed)
        setattr(x, "prev_created_on", texts[i+1].created_on)
    ctx = {"texts": texts, "url": url }
    return render(request, tpl, ctx)


@login_required
def diff(request, tpl="main/diff.html"):
    t1 = PageText.objects.filter(text_hashed=request.GET.get("1")).first()
    t2 = PageText.objects.filter(text_hashed=request.GET.get("2")).first()

    l1 = t1.text.splitlines() if t1 else [""]
    l2 = t2.text.splitlines() if t2 else [""]

    s = difflib.SequenceMatcher(None, l1, l2)
    diffs = s.get_opcodes()
    for i, [tag, i1, i2, j1, j2] in enumerate(diffs):
        print(i, tag, i1, i2, j1, j2)

    # x = difflib.ndiff(t1.text, t2.text)
    # import pdb; pdb.set_trace()

    return render(request, tpl, {"text1": t1, "text2": t2})


@login_required
def delete(request, tpl="main/del.html"):
    if request.method == "POST":
        PageUrl.objects.get(pk=request.POST["pk"]).delete()
        return HttpResponseRedirect(reverse("home"))
    return HttpResponseNotFound()


@login_required
def add(request, tpl="main/add.html"):
    if request.method == "POST":
        form = AddUrlForm(request.POST)
        if form.is_valid():
            page_url = PageUrl(url=form.cleaned_data["url"])
            page_url.save()
    return HttpResponseRedirect(reverse("home"))
