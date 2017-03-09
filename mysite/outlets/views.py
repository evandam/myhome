from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Outlet
import logging

logger = logging.getLogger(__name__)

def index(request):
    outlets = Outlet.objects.all()
    for o in outlets:
        o.state = 'on' if o.state else 'off'
    return render(request, 'outlets/index.html', {'outlets': outlets})

def list(request):
    '''
    List all outlets registered in JSON
    '''
    outlets = Outlet.objects.all()
    d = []
    for outlet in outlets:
        d.append({
            'id': outlet.id,
            'name': outlet.name,
            'state': outlet.state
        })
    return JsonResponse({'outlets': d})

def _sendsignal(outlet_id, state):
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    res = {
        'outlet_name': outlet.name,
        'outlet_id': outlet.id,
        'status': True
    }
    status = 200
    try:
        outlet.turn_on() if state else outlet.turn_off()
        res['message'] = '{} turned {} successfully'.format(
            outlet.name, 'on' if outlet.state else 'off')
    except Exception as e:
        res['message'] = str(e)
        res['status'] = False
        status = 500
    return JsonResponse(res, status=status)

def turn_on(request, outlet_id):
    return _sendsignal(outlet_id, True)

def turn_off(request, outlet_id):
    return _sendsignal(outlet_id, False)
