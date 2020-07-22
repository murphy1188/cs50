from django.shortcuts import render
from django import forms
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
from . import util
from markdown2 import Markdown
import random

markdown = Markdown()

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.convert(util.get_entry(entry)),
            "title": entry.capitalize() 
    })
    else:
        error = HttpResponseNotFound()
        return render(request, "encyclopedia/not_found.html", {
            "error": error
        })

def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        entries_case = []
        for entry in util.list_entries():
            lc = entry.lower()
            entries_case.append(lc)

        if query.lower() in entries_case:
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown.convert(util.get_entry(query)),
                "title": query.capitalize()
                })
        else: 
            results_list = []
            for entry in util.list_entries():
                lc = entry.lower()
                if lc.find(query.lower()) != -1:
                    results_list.append(entry)
            return render(request, "encyclopedia/search.html", {
                "query": query, "entries": util.list_entries(), "results": results_list
                })
    else:
        return render(request, "encyclopedia/not_found.html")

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entries = []
            for entry in util.list_entries():
                lc = entry.lower()
                entries.append(lc)
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title.lower() not in entries:
                util.save_entry(title, content)
            else:
                messages.error(request, "Error: Title already exists")
                return render(request, "encyclopedia/new_page.html", {
                    "newPageForm": form
                })
        return HttpResponseRedirect(reverse("wiki:page", args=(title,)))
    
    return render(request, "encyclopedia/new_page.html", {
        "newPageForm": NewPageForm()
    })

def edit(request, title):
    content = util.get_entry(title)
    form = EditPageForm(initial={'title': title, 'content': content})
    if request.method == "GET":
        #content = util.get_entry(title)
        #form = EditPageForm(initial={'title': title, 'content': content})
        return render(request, "encyclopedia/edit.html", {
            "form": form
        })
    elif request.method == "POST":
        edits = EditPageForm(request.POST)
        if edits.is_valid():
            title = edits.cleaned_data["title"]
            content = edits.cleaned_data["content"]
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse("wiki:page", args=(title,)))
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": form
        })


def rand(request):
    entryList = []
    for entry in util.list_entries():
        entryList.append(entry)
    rando = random.choice(entryList)
    return HttpResponseRedirect(reverse("wiki:page", args=(rando,)))
    