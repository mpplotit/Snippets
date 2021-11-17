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
               'snippets': snippets,
               'count': len(snippets)
               }
    return render(request, 'pages/view_snippets.html', context)


def show_snippet(request, snippet_number):
    try:
        snippet = Snippet.objects.get(id=snippet_number)
    except ObjectDoesNotExist:
        raise Http404
    context = {'pagename': f'Просмотр сниппета №{snippet_number}',
               'snippet': snippet,
               'type': 'view'
               }
    return render(request, 'pages/snippet.html', context)


def create_new_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list")
        return render(request, 'add_snippet.html', {'form': form})


def delete_snippet(request, snippet_number):
    try:
        snippet = Snippet.objects.get(id=snippet_number)
    except ObjectDoesNotExist:
        raise Http404
    snippet.delete()
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets
               }
    return render(request, 'pages/view_snippets.html', context)


def modify_snippet(request, snippet_number):
    try:
        snippet = Snippet.objects.get(id=snippet_number)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'GET':
        context = {'pagename': f'Просмотр сниппета №{snippet_number}',
                   'snippet': snippet,
                   'type': 'edit'
                   }
        return render(request, 'pages/snippet.html', context)
    if request.method == 'POST':
        form_data = request.POST
        snippet.name = form_data['name']
        snippet.creation_date = form_data['creation_date']
        snippet.code = form_data['code']
        snippet.save()

    return redirect('snippets-list')
