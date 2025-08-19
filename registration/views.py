from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from .models import Participant
from .forms import ParticipantForm
import base64

def register(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            
            # Handle camera photo data
            photo_data = request.POST.get('photo_data')
            if photo_data and photo_data.startswith('data:image'):
                format, imgstr = photo_data.split(';base64,')
                ext = format.split('/')[-1]
                photo_file = ContentFile(base64.b64decode(imgstr), name=f'photo_{participant.first_name}_{participant.last_name}.{ext}')
                participant.photo = photo_file
            
            participant.save()
            return redirect('id_card', pk=participant.pk)
    else:
        form = ParticipantForm()
    return render(request, 'registration/register.html', {'form': form})

def id_card(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    return render(request, 'registration/id_card.html', {'participant': participant})

def bulk_print(request):
    start_id = request.GET.get('start', 1)
    try:
        start_id = int(start_id)
        participants = Participant.objects.filter(camp_id__range=[start_id, start_id + 11]).order_by('camp_id')[:12]
        return render(request, 'registration/bulk_print.html', {'participants': participants, 'start_id': start_id})
    except ValueError:
        participants = Participant.objects.order_by('camp_id')[:12]
        return render(request, 'registration/bulk_print.html', {'participants': participants, 'start_id': 1})