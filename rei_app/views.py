from django.shortcuts import render,redirect
from .services import searchProperties
from .models import Lead
from login_app.models import User
from django.contrib import messages
import requests
import json
# Create your views here.

def index(request):
    if 'user_id' not in request.session:
        return render(request, 'login.html')
    context = {
        'this_user' : User.objects.get(id = request.session['user_id']),
    }
    return render(request, 'index.html', context)

def my_account(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/login')
    else:
        context = {
            'this_user' : User.objects.get(id = request.session['user_id'])
        }
        return render(request, "my_account.html", context)


def rental_type(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/login')
    else:
        context = {
            'this_user': User.objects.get(id = request.session['user_id'])
        }
        return render(request, 'market_search.html', context)


def rental_parse(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/login')
    else:
        if request.POST['rental_type'] == "traditional":
            state_code = request.POST['state']
            url = "https://mashvisor-api.p.rapidapi.com/city/top-markets"
            querystring = {"state":f"{state_code}","items":"5"}
            headers = {
                'x-rapidapi-key': "",
                'x-rapidapi-host': "mashvisor-api.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            markets = response.json()
            print(markets)
            context = {
                'this_user' : User.objects.get(id = request.session['user_id']),
                'long_markets' : markets['content']
            }
            return render(request,'market_search_results.html', context)
        else:
            state_code = request.POST['state']
            url = "https://mashvisor-api.p.rapidapi.com/trends/cities"
            querystring = {"state":f"{state_code}","page":"1","items":"5"}
            headers = {
                'x-rapidapi-key': "",
                'x-rapidapi-host': "mashvisor-api.p.rapidapi.com"
                }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            markets = response.json()
            context = {
                'this_user' : User.objects.get(id = request.session['user_id']),
                'short_markets' : markets['content']['cities']
            }
            return render(request, 'market_search_results.html', context)


def broad(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/login')
    else:
        context = {
            'this_user' : User.objects.get(id = request.session['user_id'])
        }
        return render(request, "broad_search.html", context)


def search_properties(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/login')
    else:
        city = request.POST['city']
        state = request.POST['state']
        prop_type = request.POST['prop_type']
        radius = request.POST['radius']
        url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
        querystring = {
            "city": f"{city}",
            "limit":"50",
            "offset":"0",
            "state_code":f"{state}",
            "sort":"price_low",
            "prop_type": f"{prop_type}",
            "radius" : f"{radius}"
        }
        headers = {
            'x-rapidapi-key': "",
            'x-rapidapi-host': "realtor.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        properties = response.json()
        properties_list = []
        for i in range (len(properties['properties'])):
            properties_list.append(properties['properties'][i])
        print(properties_list)
        context = {
            'this_user' : User.objects.get(id = request.session['user_id']),
            'properties' : properties_list
        }
        return render(request, "broad_search_results.html", context)

def create_lead(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/login')
    else:
        this_user = User.objects.get(id = request.session['user_id'])
        this_lead = Lead.objects.create(
            property_id = request.POST['property_id'],
            address = request.POST['address'],
            city = request.POST['city'],
            state = request.POST['state'],
            postal_code = request.POST['postal_code'],
            price = request.POST['price'],
            beds = request.POST['beds'],
            baths = request.POST['baths'],
            prop_type = request.POST['prop_type'],
            listing = request.POST['listing']
        )
        this_lead.investors.add(this_user)
        this_lead.save()
        return redirect('/')

def remove_lead(request, num):
    if 'user_id' not in request.session:
        messages.error('You must be logged in to view that page!')
        return redirect('/login')
    else:
        this_lead = Lead.objects.get(id = num)
        this_lead.delete()
        return redirect('/')

def investment_performance(request, state, city):
    if 'user_id' not in request.session:
        messages.error('You must be logged in to view that page!')
        return redirect('/login')
    else:
        url = f"https://mashvisor-api.p.rapidapi.com/city/investment/{state}/{city}"
        headers = {
            'x-rapidapi-key': "",
            'x-rapidapi-host': "mashvisor-api.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)
        market_data = response.json()
        context = {
            'this_user' : User.objects.get(id = request.session['user_id']),
            'market_data' : market_data['content'],
            'city' : city,
            'state' : state,
        }
        return render(request, 'investment_performance.html', context)