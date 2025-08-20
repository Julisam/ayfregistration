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
    participant_type = request.GET.get('type', 'C')
    start_range = request.GET.get('range', '1')
    
    CAMPERS = ['Executive', 'Leader', 'Delegate']
    
    try:
        start_id = int(start_range)
    except ValueError:
        start_id = 1
    
    # Filter participants by type
    if participant_type == 'C':
        all_participants = Participant.objects.filter(role__in=CAMPERS).order_by('camp_id')
    else:
        all_participants = Participant.objects.exclude(role__in=CAMPERS).order_by('camp_id')
    
    # Get participants for current range
    participants = all_participants.filter(camp_id__range=[start_id, start_id + 11])[:12]
    
    # Generate card ranges
    max_id = all_participants.last().camp_id if all_participants.exists() else 12
    card_ranges = []
    for i in range(1, max_id + 1, 12):
        end_id = min(i + 11, max_id)
        card_ranges.append({'start': i, 'end': end_id})
    
    context = {
        'participants': participants,
        'participant_type': participant_type,
        'current_start': start_id,
        'current_end': min(start_id + 11, max_id),
        'card_ranges': card_ranges[::-1],
    }
    
    return render(request, 'registration/bulk_print.html', context)

def bulk_voucher(request):
    CAMPERS = ['Executive', 'Leader', 'Delegate']
    participants = Participant.objects.filter(role__in=CAMPERS).order_by('camp_id')
    
    context = {
        'participants': participants,
    }
    
    return render(request, 'registration/bulk_voucher.html', context)