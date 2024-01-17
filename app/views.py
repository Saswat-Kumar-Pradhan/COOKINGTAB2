from django.shortcuts import render,redirect
from .models import Event, Profile, Purchase, Contribution
from django.db.models import Sum

# Create your views here.

def home(request):
    events = Event.objects.all().order_by('-id')
    profiles = Profile.objects.all()
    event_contributions = Contribution.objects.all()

    if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        contributors = request.POST.getlist('contributors')
        new_event = Event(subject=subject, date=date)
        new_event.save()
        current_event = Event.objects.get(subject=subject, date=date)
        for contributor in contributors:
            user = Profile.objects.get(pk=contributor)
            new_data = Contribution(event=current_event, profile=user, amount=0)
            new_data.save()
        return redirect('/')
    context={'events':events, 'profiles':profiles,'event_contributions':event_contributions}
    return render(request, 'home.html', context)

def addProfile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        profile_pic = request.FILES.get('profile_pic')
        profile = Profile.objects.create(name=name, profile_pic=profile_pic)
        profile.save()
        return redirect('/')
    return render(request, 'addProfile.html')

def eventDetails(request, event_id, y):
    event = Event.objects.get(pk=event_id)
    profiles = Contribution.objects.filter(event=event.id).all()
    # print(profiles.count())
    # total_price = Purchase.objects.filter(event=event.id).aggregate(Sum('price'))['price__sum']
    # print(total_price)
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
    context={'event':event,'event_contributions':event_contributions, "event_purchase":event_purchase,'x':x}
    return render(request, 'eventDetails.html', context)