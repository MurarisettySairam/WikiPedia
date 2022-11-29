from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2 as md

from . import util

class EntityForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_content(request,title):
    try:
        content = util.get_entry(title)

        return render(request, "encyclopedia/wiki.html",{
            "title": title,
            "content": content
        })

    except:
        content = "Wrong path"
        
        return render(request, "encyclopedia/wiki.html",{
            "title": title,
            "content": content,
            "message": "lol"
        })

def search(request):
    if request.method == "POST":
        searched = request.POST.get("q", "")
        result_list = []
        if util.get_entry(searched):
            return get_content(request,searched)
        else:
            for x in util.list_entries():
                if searched.lower() == x[:len(searched)].lower():
                    result_list.append(x)

    return render(request, "encyclopedia/search.html",{
        "result_list": result_list
    })

def creating(request):
    if request.method == "POST":
        form = EntityForm(request.POST)
        message =""
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title)):
                message = "this title already exists"
                return render(request,"encyclopedia/create.html",{
                    "form":form,
                    "message":message
                })
            else:
                util.save_entry(title,content)
                return get_content(request,title)

        else:
            return render(request,"encyclopedia/create.html",{
                "form":form
            })

    return render(request, "encyclopedia/create.html",{
        "form": EntityForm()
    })

def editing(request):

    if request.method == "POST":
        form = EntityForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title,content)
            get_content(request,title)

        return get_content(request,title)
    
    else:
        return render(request,"encyclopedia/edit.html",{
            "message":"Something went wrong.",
            "form":form
        })
        
def initialize_form(request, title):
    InitialForm = EntityForm(initial={'title': title, 'content':util.get_entry(title)})
    return render(request,"encyclopedia/edit.html",{ 
        "form":InitialForm
    })

def random_pages(request):
    all_entries = util.list_entries()
    entry = random.choice(all_entries)

    return render(request, "encyclopedia/wiki.html",{
        "title": entry,
        "content":util.get_entry(entry)
    })

def get_markdown(self):
    content = self.content
    return md(content)