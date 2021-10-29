from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util
import markdown
import random


# Create your views here.
# Home Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



# New Article
class NewArticleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), max_length=150)
    content = forms.CharField(widget=forms.Textarea(attrs={'size': '20'}))

def NewArticle(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            title = title.capitalize()
            content = form.cleaned_data["content"]
            #save new file
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "new", {
                "form": NewArticleForm()
            })

    return render(request, "encyclopedia/new.html", {
        "form": NewArticleForm()
    })

# Article page
def pages(request, title):
    content = util.get_entry(title)

    if content == None:
        return HttpResponseNotFound()
    else:
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": markdown.markdown(content)

        })

# Edit article
def edit(request, title):
    content = util.get_entry(title)

    if content == None:
        return HttpResponseNotFound()
    else:
        old_article = {'title': title, 'content': content}
        oldArticleForm = NewArticleForm(old_article)
        oldArticleForm.fields['title'].widget.attrs['readonly'] = True
        return render(request, "encyclopedia/edit.html", {
            "form": oldArticleForm,
            "title": old_article['title']
        })

# Save edition article
def saveEdit(request, title):
    if request.method == "POST":
        updArticle = request.POST
        content = updArticle.get('content')
        util.save_entry(title, content)

    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": markdown.markdown(content)
    })

# Random Article
def randomArticle(request):
    list = util.list_entries()
    rnd_title = random.choice(list)
    if rnd_title == None:
        return HttpResponseNotFound()
    else:
        return HttpResponseRedirect(reverse("pages", args=[rnd_title]))

# Search Article
def search(request):
    search_title = request.GET.get('q')
    #search_title = search_title.capitalize()
    list_article = util.list_entries()

    for title in list_article:
        #search subRow 'search_title' into the Row 'title' (or capitalize one)
        part_title_cap = title.find(search_title.capitalize())
        part_title = title.find(search_title)

        #if found - retutn page about title
        if part_title_cap != -1 or part_title != -1:
            content = util.get_entry(title)

            return render(request, "encyclopedia/page.html", {
                "title": title,
                "content": markdown.markdown(content)
            })
    # if user typed wrong title - render page with error
    if search_title not in list_article:
        return render(request, "encyclopedia/search.html", {
            "title": search_title
        })        

