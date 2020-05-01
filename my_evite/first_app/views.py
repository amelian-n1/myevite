from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.db.models import Count
from time import gmtime, strftime
from .models import User, Event, Guest, RSVP
from datetime import date
import bcrypt
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 

            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
            messages.success(request, "Your registration is complete.")
            return redirect('/')

def login(request):

    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            request.session['first_name'] = logged_user.first_name
            return redirect('/newEvent')
    else:
        messages.error(request, "User not found.")
        return redirect('/')

def dashboard(request):
    if 'userid' in request.session:
        context = {
            'userid': request.session['userid'],
            'first_name': request.session['first_name'],
            'upcoming_events': Event.objects.filter(host=request.session['userid']).filter(date__gte=date.today()).order_by("date").all(),
            'past_events': Event.objects.filter(host=request.session['userid']).filter(date__lt=date.today()).order_by("date").all(),
            'host': User.objects.filter(id=request.session['userid']),
            'yes_number': RSVP.objects.filter(response="yes").count()
        }
        return render(request, 'dashboard.html', context)
    return render(request, 'dashboard.html')

def newEvent(request):
    if 'userid' in request.session:
        context = {
        }
        return render(request,'new_event.html')
    return render(request,'/')

def createEvent(request):
    if request.method == "POST":
        errors = Event.objects.eventValidate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/newEvent')
        else:
            event = Event.objects.create(
                title=request.POST['title'],
                details=request.POST['details'],
                date=request.POST['date'],
                start_time=request.POST['start_time'],
                end_time=request.POST['end_time'],
                line1=request.POST['line1'],
                line2=request.POST['line2'],
                city=request.POST['city'],
                state=request.POST['state'],
                zip=request.POST['zip'],
                host=User.objects.get(id=request.session['userid'])
            )
            return redirect('/dashboard')

def evite(request,id):
    
    context = {
        'event': Event.objects.filter(id=id),
        'host': User.objects.filter(id=request.session['userid']),
        'api_key': settings.GOOGLE_MAPS_API_KEY
    }
    
    return render(request,'evite.html',context)

def eventDetails(request,id):
    
    context = {
        'event': Event.objects.get(id=id),
        
    }
    return render(request,'event_detail.html', context)

def delete(request, id):
    event = Event.objects.filter(id=id)
    event.delete()
    return redirect('/dashboard')

def rsvp(request):
    if request.method == "POST":
        errors = Guest.objects.guest_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            event_id = request.POST['event_id']
            return redirect('/evite/{}'.format(event_id))
        
        else:
            form_email = request.POST['email']
            returning_guest = Guest.objects.filter(email=form_email)

            if returning_guest:

                form_first_name = request.POST['first_name']
                same_name_guest = Guest.objects.filter(email=form_email, first_name=form_first_name)

                if same_name_guest:

                    same_name_guest = Guest.objects.get(email=form_email, first_name=form_first_name)

                    event_id = request.POST['event_id']
                    this_event = Event.objects.get(id=event_id)

                    guest_rsvp = RSVP.objects.filter(guest=same_name_guest, event=this_event)

                    if guest_rsvp:
                    
                        guest_rsvp = RSVP.objects.get(guest=same_name_guest, event=this_event)
                        guest_rsvp.response = request.POST['response']
                        guest_rsvp.save()
                        messages.success(request, "Thank you for updating your RSVP!")
                        return redirect('/evite/{}'.format(event_id))

                    else:

                        request.session['guestid'] = same_name_guest.id

                        rsvp = RSVP.objects.create(
                            guest = Guest.objects.get(id=request.session['guestid']),
                            event = this_event,
                            response = request.POST['response']
                        )
                        messages.success(request, "Thank you for your RSVP!")
                        return redirect('/evite/{}'.format(event_id))

                else:

                    event_id2 = request.POST['event_id']

                    messages.error(request, 'This email address is already in use by another guest. Update your information and try again.')

                    return redirect('/evite/{}'.format(event_id2))

            else:
                
                event_id = request.POST['event_id']

                guest = Guest.objects.create(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email']
                )

                request.session['guestid'] = guest.id
                event = Event.objects.get(id=event_id)

                rsvp = RSVP.objects.create(
                    guest = Guest.objects.get(id=request.session['guestid']),
                    event = event,
                    response = request.POST['response']
                )
                messages.success(request, "Thank you for your RSVP!")
                
                return redirect('/evite/{}'.format(event_id))

