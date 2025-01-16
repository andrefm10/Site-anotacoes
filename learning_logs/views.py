from django.shortcuts import render
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
#Decorator é uma forma simples de alterar comportamento de uma funcao sem mudar codigo.

# Create your views here.

def index(request):
    """pagina principal do site"""
    return render(request, 'learning_logs/index.html')

def erro(request):
    """pagina de 404"""
    return render(request, 'learning_logs/404.html')

@login_required #preciso setar nas settings.py a pagina de login para o django saber p onde redirecionar
def topics(request):
    """pagina quando dou /topics no navegador"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') #filtrar para que possa ser unico para cada user
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request,topic_id): #id da entrie especifica
    """pagina de assunto unico"""
    topic = Topic.objects.get(id = topic_id)
    #garante que o assunto pertecera ao usuario certo
    if topic.owner != request.user:
        return HttpResponseRedirect(reverse('404'))
        
    entries = topic.entry_set.order_by('-date_added') # " - " muda a ordem q agora será de mais recente a mais antigo
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Possibita um usuário comum a adicionar seus tópicos"""
    if request.method != 'POST': 
        #Nesse caso, nenhum dado é submetido, então criamos um formulario em branco
        form = TopicForm()
    else:
        #Dados de POST submetidos, então processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics')) #manda automaticamente pra pagina principal dos topics
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """Possibilita um usuário comum a adicionar as anotações dos topicos"""
    topic = Topic.objects.get(id=topic_id)
    
    #garante que o assunto pertecera ao usuario certo
    if topic.owner != request.user:
        return HttpResponseRedirect(reverse('404'))
    
    if request.method != 'POST':
        #Nesse caso, nenhum dado é submetido, então criamos um formulario em branco
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required    
def edit_entry(request,entry_id):
    """Possibilita um usuário a editar suas anotações"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    #garante que o assunto pertecera ao usuario certo
    if topic.owner != request.user:
        return HttpResponseRedirect(reverse('404'))

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form} #tudo q a pagina poderá usar 
    return render(request,'learning_logs/edit_entry.html',context)
