from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def get_game_state(session):
    return {
        'gold': session.get('gold', 0),
        'gpc': session.get('gpc', 1), 
        'upgrade_gpc_price': session.get('upgrade_gpc_price', 10),
        'cps': session.get('cps', 0), 
        'buy_cps_price': session.get('buy_cps_price', 100), 
        'buy_cps_amount': session.get('buy_cps_amount', 1), 
    }

def set_game_state(session, state):
    session['gold'] = state['gold']
    session['gpc'] = state['gpc']
    session['upgrade_gpc_price'] = state['upgrade_gpc_price']
    session['cps'] = state['cps']
    session['buy_cps_price'] = state['buy_cps_price']
    session['buy_cps_amount'] = state['buy_cps_amount']
    session.modified = True

def cookie_clicker_game(request):
    state = get_game_state(request.session)
    return render(request, 'cookie_clicker/game.html', state)

@csrf_exempt # For simplicity in this example, but in production, use proper CSRF, na solbad najd HAHAHA
def click_cookie(request):
    if request.method == 'POST':
        state = get_game_state(request.session)
        state['gold'] += state['gpc']
        set_game_state(request.session, state)
        return JsonResponse(state) # Return updated state as JSON
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def upgrade_gpc(request):
    if request.method == 'POST':
        state = get_game_state(request.session)
        if state['gold'] >= state['upgrade_gpc_price']:
            state['gold'] -= state['upgrade_gpc_price']
            state['gpc'] += 1 # i++ 
            state['upgrade_gpc_price'] = int(state['upgrade_gpc_price'] * 1.5) # Price increase
            set_game_state(request.session, state)
            return JsonResponse(state)
        return JsonResponse({'error': 'Not enough gold'}, status=403)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def buy_auto_clicker(request):
    if request.method == 'POST':
        state = get_game_state(request.session)
        if state['gold'] >= state['buy_cps_price']:
            state['gold'] -= state['buy_cps_price']
            state['cps'] += state['buy_cps_amount'] # Add auto click amount, kapoy huna2 sa logic huuhuh
            state['buy_cps_price'] = int(state['buy_cps_price'] * 1.8) 
            set_game_state(request.session, state)
            return JsonResponse(state)
        return JsonResponse({'error': 'Not enough gold'}, status=403)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def auto_generate_gold(request):
    if request.method == 'POST':
        state = get_game_state(request.session)
        state['gold'] += state['cps'] 
        set_game_state(request.session, state)
        return JsonResponse(state)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def reset_game(request):
    if request.method == 'POST':
        request.session['gold'] = 0
        request.session['gpc'] = 1
        request.session['upgrade_gpc_price'] = 10
        request.session['cps'] = 0
        request.session['buy_cps_price'] = 100
        request.session['buy_cps_amount'] = 1
        request.session.modified = True
        return JsonResponse(get_game_state(request.session))
    return JsonResponse({'error': 'Invalid request method'}, status=400)