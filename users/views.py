from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def logout_view(request): 
    #Faz um logout do usuário
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    #Faz o cadastro de um novo usuario
    if request.method != 'POST':
        # Exibe o formulario em branco
        form = UserCreationForm()
    else:
        # Processa o formulario preenchido
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #Faz o login do usuario e volta a tela principal do site
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)

