# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from .forms import RoomForm

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})

def edit_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'edit_room.html', {'form': form})

def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'delete_room.html', {'room': room})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


from django.shortcuts import render
from .models import Room


from .models import Room
from django.shortcuts import render, redirect

def search_rooms(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        room_type = request.GET.get('room_type')

        # Perform room availability check based on start date and room type
        available_rooms = Room.objects.filter(type=room_type, available_seat__gt=0)

        context = {
            'start_date': start_date,
            'room_type': room_type,
            'available_rooms': available_rooms,
        }
        return render(request, 'search_room.html', context)

