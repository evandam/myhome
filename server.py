import json
import logging
from flask import Flask, render_template
from ConfigParser import ConfigParser
from switch import Switch

logging_format = '%(asctime)-15s %(filename)s %(levelname)s %(message)s'
logging.basicConfig(filename='logs/app.log', format=logging_format)
logger = logging.getLogger(__name__)

app = Flask(__name__)
globals = {}

def load_switches():
    config = ConfigParser()
    config.read('switches.conf')
    globals['switches'] = []
    i = 0 # ID for switches
    for name in config.sections():
        oncode = config.get(name, 'on')
        offcode = config.get(name, 'off') 
        globals['switches'].append(Switch(i, name, oncode, offcode))
        i += 1
    logger.info('Loaded switches: {}'.format(globals['switches']))

load_switches()

def get_switch(id):
    '''
    Lookup a switch by ID. Raise exception if not found.
    '''
    switch = filter(lambda x: x.id == id, globals['switches'])
    if len(switch) > 0:
        return switch[0]
    else:
        e = 'Could not find switch with ID: {}'.format(id)
        logger.warn(e)
        raise Exception(e)

@app.route('/')
def index():
    '''
    Home page
    '''
    return render_template('index.html', switches=globals['switches'])

@app.route('/api/switch')
def list_switches():
    '''
    Get list of switches (names and IDs) that can be controlled
    '''
    return json.dumps([{'id': x.id, 'name': x.name} for x in globals['switches']])

@app.route('/api/switch/<int:switch_id>/<state>')
def toggle_switch(switch_id, state):
    '''
    Lookup a switch and try to toggle to a given state
    '''
    response = {}
    state = state.lower().strip()
    try:
        switch = get_switch(switch_id)
        if state == 'on':
            switch.on()
            response['message'] = '{} turned on!'.format(switch.name)
        elif state == 'off':
            switch.off()
            response['message'] = '{} turned off!'.format(switch.name)
        else:
            response['error'] = '{} not a valid state'.format(state)
    except Exception as e:
        logger.exception(e)
        response['error'] = str(e)
    
    if 'error' in response:
        return json.dumps(response), 400 # BAD REQUEST
    else:
        response['switch'] = {'id': switch.id, 'name': switch.name}
        response['state'] = state
        return json.dumps(response)
        
@app.route('/refresh')
def refresh():
    load_switches()
    return "Refreshed list of switches!"

if __name__ == '__main__':
    app.run()
