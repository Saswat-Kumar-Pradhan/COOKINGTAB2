from django.shortcuts import render,redirect
from .models import Event, Profile, Purchase, Contribution, Tab
from django.db.models import Sum
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage
from django.contrib import messages
import os


# Create your views here.

def loginSignup(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            tabname = request.POST.get('tabname')
            psd = request.POST.get('pswd')
            try:
                tab_instance = Tab.objects.get(name=tabname, password=psd)
                return redirect('/home')
            except:
                pass
        elif 'register' in request.POST:
            tabname = request.POST.get('tabname')
            email = request.POST.get('email')
            psd = request.POST.get('pswd')
            Tab.objects.create(name=tabname, email=email, password=psd)
            return redirect('/')
    return render(request, 'loginSignup.html')


def signup(request):
    if request.method == 'POST':
        tabname = request.POST.get('tabname')
        email = request.POST.get('email')
        psd = request.POST.get('pswd')
        Tab.objects.create(name=tabname, email=email, password=psd)
        return redirect('/loginSignup')
    return render(request, 'loginSignup.html')


def home(request):
    events = Event.objects.all().order_by('-id')
    profiles = Profile.objects.all()
    event_contributions = Contribution.objects.all()

    for profile in profiles:
        paid = Purchase.objects.filter(profile=profile.id).aggregate(Sum('price'))['price__sum']
        total = Contribution.objects.filter(profile=profile.id).aggregate(Sum('amount'))['amount__sum']
        profile.paid = paid if paid else 0
        profile.total = total if total else 0
        profile.due = profile.paid - profile.total if profile.paid is not None and profile.total is not None else 0

    if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        contributors = request.POST.getlist('contributors')
        if contributors != []:
            new_event = Event(subject=subject, date=date)
            new_event.save()
            current_event = Event.objects.get(subject=subject, date=date)
            for contributor in contributors:
                user = Profile.objects.get(pk=contributor)
                new_data = Contribution(event=current_event, profile=user, amount=0)
                new_data.save()
        return redirect('/home')
    context={'events':events, 'profiles':profiles,'event_contributions':event_contributions}
    return render(request, 'home.html', context)


def addProfile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        profile_pic = request.FILES.get('profile_pic')
        image = Image.open(profile_pic)
        size = min(image.size)
        left = (image.width - size) / 2
        top = (image.height - size) / 2
        right = (image.width + size) / 2
        bottom = (image.height + size) / 2
        image = image.crop((left, top, right, bottom))
        thumb_io = BytesIO()
        image.save(thumb_io, format='PNG')
        thumb_path = f'profile_pics/{name}_profile_pic.jpg'
        default_storage.save(thumb_path, thumb_io)
        profile = Profile.objects.create(name=name, profile_pic=thumb_path)
        profile.save()
        return redirect('/home')
    return render(request, 'addProfile.html')


def profileDetails(request, profile_id):
    message = messages.get_messages(request)
    profile = Profile.objects.get(pk=profile_id)
    event_contributions = Contribution.objects.filter(profile=profile).all()
    event_purchase = Purchase.objects.filter(profile=profile).all()
    context={'profile':profile,'event_contributions':event_contributions, "event_purchase":event_purchase,'messages': message}
    return render(request, 'profileDetails.html', context)


def editProfileDetails(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        profile_pic = request.FILES.get('profile_pic')
        image = Image.open(profile_pic)
        size = min(image.size)
        left = (image.width - size) / 2
        top = (image.height - size) / 2
        right = (image.width + size) / 2
        bottom = (image.height + size) / 2
        image = image.crop((left, top, right, bottom))
        thumb_io = BytesIO()
        image.save(thumb_io, format='PNG')
        thumb_path = f'profile_pics/{profile_id}_profile_pic.png'
        if profile.profile_pic:
                profile.profile_pic.delete()
        default_storage.save(thumb_path, thumb_io)
        profile.profile_pic = thumb_path
        profile.name = name
        profile.save()
        return redirect('/home')
    context={'profile':profile}
    return render(request, 'editProfile.html', context)


def deleteProfileDetails(request, profile_id):
    current_profile = Profile.objects.get(pk=profile_id)
    contributions = Contribution.objects.filter(profile=profile_id)
    purchases = Purchase.objects.filter(profile=profile_id)
    if contributions.exists() or purchases.exists():
        messages.warning(request, "Can't delete. There are some pending amounts in the events.")
        return redirect('profileDetails', profile_id)
    if current_profile.profile_pic:
        current_profile.profile_pic.delete()
    current_profile.delete()
    return redirect('home')


def eventDetails(request, event_id, y):
    event = Event.objects.get(pk=event_id)
    profiles = Contribution.objects.filter(event=event.id).all()
    all_profiles = Profile.objects.all()
    profile_ids = profiles.values_list('profile_id', flat=True)
    event_contributions = Contribution.objects.all()
    event_purchase = Purchase.objects.filter(event = event).all()
    x=(Event.objects.count()+1-y)%5
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        products = request.POST.get('products')
        price = request.POST.get('price')
        user = Profile.objects.get(pk=profile_id)
        purchase = Purchase.objects.create(event=event, profile=user, products=products, price=price)
        purchase.save()

        total_price = Purchase.objects.filter(event=event.id).aggregate(Sum('price'))['price__sum']
        per_user_price = total_price / profiles.count()

        Contribution.objects.filter(event=event.id).update(amount=per_user_price)
        return redirect('eventDetails', event_id, y)
    context={'event':event,'event_contributions':event_contributions,'profile_ids': profile_ids, "event_purchase":event_purchase,'x':x, 'profiles':profiles, 'all_profiles':all_profiles}
    return render(request, 'eventDetails.html', context)


def editEventDetails(request, event_id, y):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        contributors = request.POST.getlist('contributors')
        if contributors != []:
            current_event = Event.objects.get(pk=event_id)
            current_event.date = date
            current_event.subject = subject
            current_event.save()
            if Purchase.objects.filter(event=event_id):
                total_price = Purchase.objects.filter(event=event_id).aggregate(Sum('price'))['price__sum']
                per_user_price = total_price / len(contributors)
            else:
                per_user_price = 0

            contributions_to_delete = Contribution.objects.filter(event=current_event)
            contributions_to_delete.delete()

            for contributor in contributors:
                user = Profile.objects.get(pk=contributor)
                new_data = Contribution(event=current_event, profile=user, amount=per_user_price)
                new_data.save()
        return redirect('eventDetails', event_id, y)
    
def deleteEventDetails(request, event_id):
    current_event = Event.objects.get(pk=event_id)
    current_event.delete()
    return redirect('home')

def timer(request):
    return render(request, 'timer.html')