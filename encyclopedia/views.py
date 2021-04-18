from django.shortcuts import render
from markdown2 import Markdown
import random
from . import util
from django.shortcuts import redirect

from django import forms

class CreatePage(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-content'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if request.method == "GET":
        page = util.get_entry(title)
        if not page:
            return render(request, "encyclopedia/dne.html")
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "page": markdowner.convert(page),
            "title": title
        })


def create(request):
    if request.method == "POST":
        form = CreatePage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/alreadyexist.html")
            file = f"entries/{title}.md"
            with open(file, mode="w") as f:
                f.write(content)
            return redirect("/wiki/" + title)
    return render(request, "encyclopedia/createpage.html", {
        "form": CreatePage()
    })

def edit(request):
    if request.method == "POST":
        title = request.POST.get('title').capitalize()
        newcontent = request.POST.get('textarea')
        if not newcontent:
            with open(f"entries/{title}.md", mode='r') as f:
                content = f.readlines()
                return render(request, "encyclopedia/edit.html", {
                    "content" : content,
                    "title" : title
                })
        else:
            with open(f"entries/{title}.md",mode="w") as f:
                f.write(newcontent)
            return redirect("/wiki/" + title)

def searchq(request):
    if request.method == "POST":
        search = request.POST.get("q").lower()
        spages = []
        fullpages = []
        pages = util.list_entries()
        for page in pages:
            if search == page.lower():
                return redirect("/wiki/" + page.capitalize())
            else:
                if search in page.lower():
                    spages.append(page)
        print(spages)
        print(fullpages)
        return render(request, "encyclopedia/search.html", {
            "spages": spages
        })

def randomp(request):
    pages = util.list_entries()
    page = random.choice(pages)
    return redirect("/wiki/" + page)