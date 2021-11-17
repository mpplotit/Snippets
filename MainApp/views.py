from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {'pagename': 'Добавление нового сниппета',
               'form': form}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets
               }
    return render(request, 'pages/view_snippets.html', context)


def show_snippet(request, snippet_number):
    try:
        snippet = Snippet.objects.get(id=snippet_number)
    except ObjectDoesNotExist:
        raise Http404
    context = {'pagename': f'Просмотр сниппета №{snippet_number}',
               'snippet': snippet
               }
    return render(request, 'pages/snippet.html', context)


def create_new_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list")
        return render(request, 'add_snippet.html', {'form': form})

