from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required 

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
	return render(request, 'learning_logs/index.html')

 
def topics(request):
	"""show all topics"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

 
def topic(request, topic_id):
	"""show one single topic"""
	topic = Topic.objects.get(id=topic_id)
	

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

 
def new_topic(request):
	if request.method != 'POST':
		form = TopicForm()
	else:
		#deal with the data
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

 
def new_entry(request, topic_id):
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		form = EntryForm()
	else:
		#deal with the data
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.owner = request.user
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', 
										args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

 
def edit_entry(request, entry_id):

	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))


	context = {'entry': entry, 'topic': topic, 'form': form}

	return render(request, 'learning_logs/edit_entry.html', context)

