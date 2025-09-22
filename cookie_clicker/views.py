from django.shortcuts import render

# Initial state sa ga,e
def cookie_clicker_game(request):
    # Initialize gold if not in session
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'gpc' not in request.session:
        request.session['gpc'] = 1 # Gold per click
    if 'upgrade_price' not in request.session:
        request.session['upgrade_price'] = 10

    context = {
        'gold': request.session['gold'],
        'gpc': request.session['gpc'],
        'upgrade_price': request.session['upgrade_price'],
    }
    return render(request, 'cookie_clicker/game.html', context)