import os

def shared_environment(request):
    
    return {
        'WEBSOCKET_URL': os.environ.get('WEBSOCKET_URL', 'ws://localhost:8000/ws/'),
    }