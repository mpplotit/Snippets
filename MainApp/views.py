from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {'pagename': 'Добавление нового сниппета',
               'form': form}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
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
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")
        return render(request, 'add_snippet.html', {'form': form})


def delete_snippet(request, snippet_number):
    try:
        snippet = Snippet.objects.get(id=snippet_number)
    except ObjectDoesNotExist:
        raise Http404
    if snippet.user == request.user:
        snippet.delete()
    else:
        raise HttpResponseForbidden
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
        if snippet.user == request.user:
            form_data = request.POST
            public = form_data.get("public") == 'on'
            snippet.name = form_data['name']
            snippet.creation_date = form_data['creation_date']
            snippet.code = form_data['code']
            snippet.public = public
            snippet.save()
        else:
            raise HttpResponseForbidden

    return redirect('snippets-list')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            context = {
                'errors': ['неверный логин или пароль'],
                'pagename': 'PythonBin'
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def my_snippets_page(request):
    userid = request.user

    if request.user.is_authenticated:
        snippets = Snippet.objects.filter(user=userid)
    else:
        snippets = Snippet.objects.all()

    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets,
               'count': len(snippets)
               }
    return render(request, 'pages/view_snippets.html', context)


def register(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {'pagename': 'Регистрация пользователя',
                   'form': form
                   }
        return render(request, 'pages/register.html', context)
    else:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context = {'pagename': 'Регистрация пользователя',
                   'form': form
                   }
        return render(request, 'pages/register.html', context)
