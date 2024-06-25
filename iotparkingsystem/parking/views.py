from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import JsonResponse
import serial 




def index(request):
    return render(request, 'index.html')

def description(request):
    return render(request, 'Description.html')







def signup(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       email    = request.POST['email']
       data = User.objects.create_user(username=username, password=password, email=email)
       data.save()
       return redirect('login')
    return render(request, 'signup.html')




def login(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = auth.authenticate(username=username, password=password)

       if user is not None:
           auth.login(request,user)
           return redirect('operate')

    return render(request, 'login.html')


#VIEWS FOR ARDUINO:
# Initialize serial connection (adjust COM port and baud rate as necessary)
try:
    arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
except:
    arduino = None

def slot_status(request):
    if arduino:
        arduino.write(b'status\n')
        slot_data = arduino.readline().decode('utf-8').strip()
    else:
        slot_data = "S1:1,S2:1,S3:1,S4:1"  # Default data for testing

    slot1_status = 'available' if 'S1:0' in slot_data else 'occupied'
    slot2_status = 'available' if 'S2:0' in slot_data else 'occupied'
    slot3_status = 'available' if 'S3:0' in slot_data else 'occupied'
    slot4_status = 'available' if 'S4:0' in slot_data else 'occupied'

    return render(request, 'slot_status.html', {
        'slot1_status': slot1_status,
        'slot2_status': slot2_status,
        'slot3_status': slot3_status,
        'slot4_status': slot4_status,
    })




def get_slot_status(request):
    arduino.write(b'status\n')
    slot_data = arduino.readline().decode('utf-8').strip()
    slot1_status = 'available' if 'S1:0' in slot_data else 'occupied'
    slot2_status = 'available' if 'S2:0' in slot_data else 'occupied'
    slot3_status = 'available' if 'S3:0' in slot_data else 'occupied'
    slot4_status = 'available' if 'S4:0' in slot_data else 'occupied'

    return JsonResponse({
        'slot1_status': slot1_status,
        'slot2_status': slot2_status,
        'slot3_status': slot3_status,
        'slot4_status': slot4_status,
    })



def operate(request):
    return render(request, 'operate.html')  


def control_barrier (request, action):
    if arduino:
        if action == 'open':
            arduino.write(b'open\n')
        elif action == 'close':
            arduino.write(b'close\n')
    return JsonResponse({'status': 'success'})

def logout_view(request):
    logout(request)
    return redirect('index')