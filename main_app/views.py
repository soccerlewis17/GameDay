from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Favorite, Comment
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .forms import CommentForm
import requests  # allow us to make api calls

headers = {
    "X-RapidAPI-Key": "a249ee6bfamshfb62e9b1c9d89d2p17b949jsn9d35882504fe",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
# Create your views here.
# api call functions


def get_league(id, season):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"league": id, "season": season}
    teams = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    return teams


def get_games(team, next):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"team": team, "next": next}
    games = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    return games

def get_last(team, num): 
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"team": team, "last": num, "status": "FT"}
    game = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response'][0]
    return game
    



def fix_timestamp(game):
    game['fixture']['timestamp'] = datetime.fromtimestamp(
        game['fixture']['timestamp'])
    return game


def get_team(id):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"id": id}
    team = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response'][0]
    return team


def get_squad(team_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"
    querystring = {"team": team_id}
    squad = requests.request("GET", url, headers=headers,
                             params=querystring).json()['response'][0]
    return (squad)


def find_live(team_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all", "team": team_id}
    live_game = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    return (live_game)


def get_game_info(game_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"id": game_id}
    game = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response'][0]
    return (game)


def get_game_stats(game_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
    querystring = {"fixture": game_id}
    live_stats = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response']
    return live_stats

def get_standings(league_id, season): 
    url = "https://api-football-v1.p.rapidapi.com/v3/standings"
    querystring = {"season": season, "league": league_id}
    standings = requests.request(
        "GET", url, headers=headers, params=querystring).json()['response'][0]['league']
    return standings

def home(request):
    teams = get_league(39, 2022)
    standings = get_standings(39, 2022)
    favorite_ids = []
    favorite_games = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        for favorite in favorites:
            favorite_ids.append(favorite.team_id)
            game_obj = {}
            game = get_games(favorite.team_id, 1)[0]
            fix_timestamp(game)
            game_obj["id"] = favorite.team_id
            game_obj["game"] = game
            favorite_games.append(game_obj)
    return render(request, 'home.html', {'teams': teams, 'favorites': favorite_ids, 'games': favorite_games, "standings" : standings})


@login_required
def team_detail(request, team_id):
    team = get_team(team_id)
    upcoming_games = get_games(team_id, 3)
    last_game = get_last(team_id, 1)
    fix_timestamp(last_game)
    for game in upcoming_games:
        fix_timestamp(game)
    squad = get_squad(team_id)
    live_game = find_live(team_id)
    favorite = Favorite.objects.filter(user=request.user, team_id=team_id)
    return render(request, 'team.html', {'team': team, 'upcoming': upcoming_games, 'squad': squad, 'live': live_game, 'last' : last_game, "favorite" : favorite})


def game_detail(request, game_id):
    game = get_game_info(game_id)
    fix_timestamp(game)
    comment_form = CommentForm()
    live_stats = get_game_stats(game_id)
    comments = Comment.objects.filter(game_id=game_id)
    return render(request, 'game.html', {'game': game, 'stats': live_stats, 'comment_form': comment_form, 'comments': comments})


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
    new_favorite = Favorite(team_id=team_id, user=request.user)
    new_favorite.save()
    return redirect('team_detail', team_id=team_id)


@login_required
def remove_team(request, team_id):
    team = Favorite.objects.filter(team_id=team_id, user=request.user)
    team.delete()
    return redirect('/')

@login_required
def add_comment(request, game_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.game_id = game_id
        new_comment.user = request.user
        new_comment.save()
    return redirect('game_detail', game_id=game_id)


@login_required 
def remove_comment(request, comment_id): 
  comment = Comment.objects.filter(id=comment_id)
  game_id = comment[0].game_id
  comment.delete()
  return redirect('game_detail', game_id=game_id)
    
