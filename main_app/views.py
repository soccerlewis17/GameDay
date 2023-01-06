from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Favorite, Comment
from django.contrib.auth.decorators import login_required
from datetime import datetime

import requests # allow us to make api calls
headers = {
	"X-RapidAPI-Key": "a249ee6bfamshfb62e9b1c9d89d2p17b949jsn9d35882504fe",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
# Create your views here.

def home(request):
  url = "https://api-football-v1.p.rapidapi.com/v3/teams"
  querystring = {"league": "39", "season": "2022"}
  all_teams = requests.request("GET", url, headers=headers, params=querystring).json()
  teams = all_teams['response']
  favorite_ids = []
  if request.user.is_authenticated: 
    favorites = Favorite.objects.filter(user= request.user)
    for favorite in favorites:
      favorite_ids.append(favorite.team_id)
  
  return render(request, 'home.html', {'teams' : teams, 'favorites' : favorite_ids})


@login_required
def team_detail(request, team_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"id": team_id}
    team = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response'][0]
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"team": team_id,"next": "3"}
    upcoming_games = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    #change timestamps to usable times
    for game in upcoming_games: 
      game['fixture']['timestamp'] = datetime.fromtimestamp(
          game['fixture']['timestamp'])
    url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"
    querystring = {"team": team_id}
    squad = requests.request("GET", url, headers=headers, params=querystring).json()['response'][0]
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all", "team" : team_id}
    live_game = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    return render(request, 'team.html', {'team' : team, 'upcoming' : upcoming_games, 'squad' : squad, 'live' : live_game})

def game_detail(request, game_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"id": game_id}
    game = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response'][0]
    game['fixture']['timestamp'] = datetime.fromtimestamp(
        game['fixture']['timestamp'])
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
    querystring = {"fixture": game_id}
    live_stats = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    return render(request, 'game.html', {'game' : game, 'stats' : live_stats})


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def favorite_team(request, team_id): 
  new_favorite = Favorite(team_id= team_id, user= request.user)
  new_favorite.save()
  return redirect('team_detail', team_id=team_id)


@login_required
def remove_team(request, team_id):
  team = Favorite.objects.filter(team_id=team_id, user=request.user)
  team.delete()
  return redirect('/')
