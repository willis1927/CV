from django.shortcuts import render
import markdown
from . import util
import os
from random import choice

def convert_md_to_html(data):
    content = util.get_entry(data)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, entry):
    content = convert_md_to_html(entry)
    if content == None:
        return render(request, "encyclopedia/error.html", {
                    "name": entry,
                    "message": "Entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "name": entry,
        "entry": content
        })

def search(request):

    if request.method == 'POST':
        search = request.POST['q']   
        html = convert_md_to_html(search)
        if html is not None:
            return render(request, "encyclopedia/entry.html", {
            "name": "search",
            "entry": html
            })

        else:
            list = util.list_entries()
            partial = []
            for item in list:
                if request.POST['q'].lower() in item.lower():
                    partial.append(item)
            if len(partial) == 0:
                return render(request, "encyclopedia/error.html", {
            "name": search,
            "message": f"No results found for {search}"
            })
            else: 
                return render(request, "encyclopedia/search.html", {
                "entries": partial
            })
def create(request):
    if request.method == "POST":
        title = request.POST['title']
        mdText = request.POST['mdText']
        
        if util.get_entry(title) == None:
            util.save_entry(title, mdText)
            html = convert_md_to_html(title)                      
            return render(request, "encyclopedia/entry.html", {
            "name": title,
            "entry": html
            })
        return render(request, "encyclopedia/error.html", {
                "name": entry,
                "message": "Entry already exists"
                })        
    else:   
        return render(request, "encyclopedia/create.html", {
        
    })

def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)        
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })      
    
def update(request):
    title = request.POST['title']
    content = request.POST['mdText']
    util.save_entry(title, content)
    html = convert_md_to_html(title)
    return render(request, "encyclopedia/entry.html", {
            "name": title,
            "entry": html
            })
def random(request):
    list = util.list_entries()
    entry = choice(list)
    content = convert_md_to_html(entry) 
    if content == None:
        return render(request, "encyclopedia/error.html", {
                    "name": entry,
                    "message": "Entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "name": entry,
        "entry": content
        })
