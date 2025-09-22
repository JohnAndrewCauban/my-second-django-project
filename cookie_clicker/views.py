# my-second-django-project/cookie_clicker/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# import json # Not strictly needed anymore if game_logic handles conversion
from .game_logic import CookieClickerGame # Import the new game logic class

def cookie_clicker_game(request):
    game = CookieClickerGame(request.session)
    state = game.get_state()
    return render(request, 'cookie_clicker/game.html', state)

@csrf_exempt # For simplicity in this example, but in production, use proper CSRF
def click_cookie(request):
    if request.method == 'POST':
        game = CookieClickerGame(request.session)
        state = game.click()
        return JsonResponse(state)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def upgrade_gpc(request):
    if request.method == 'POST':
        game = CookieClickerGame(request.session)
        try:
            state = game.upgrade_gpc()
            return JsonResponse(state)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=403)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def buy_auto_clicker(request):
    if request.method == 'POST':
        game = CookieClickerGame(request.session)
        try:
            state = game.buy_autoclicker()
            return JsonResponse(state)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=403)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def auto_generate_gold(request):
    if request.method == 'POST':
        game = CookieClickerGame(request.session)
        state = game.auto_generate_gold()
        return JsonResponse(state)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def reset_game(request):
    if request.method == 'POST':
        game = CookieClickerGame(request.session)
        state = game.reset()
        return JsonResponse(state)
    return JsonResponse({'error': 'Invalid request method'}, status=400)