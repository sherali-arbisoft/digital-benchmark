from django.shortcuts import render
from django.http import HttpResponse

import facebook as fb

# access_token = 'EAAMNh9MnOUoBAGSRxDPSDa6vKgTryopWZC9zg0TaCNCM2J7mxRajEfLn9TmAkHyIs0LxlEyZBXxpJZBqFhNcZA6wdeybXehd4MdgpDjiiIAgG9zjHT5ST83PlSr42CIoWlKH9iiOpsQbilJgk0czURxBxNncPzZBujC7OINkHgqhZBZANrpSPnWHYbP44fZAV994iagWZCmWpoAZDZD'
version = '3.1'

# Create your views here.
def feed(request, access_token):
    graph = fb.GraphAPI(access_token=access_token, version=version)
    feed = graph.get_connections(id='me', connection_name='feed')
    response = '<ul>'
    for post in feed['data']:
        response += '<li>' + post.get('created_time', '') + ' ' + post.get('id', '') + ': ' + post.get('message', '') + '</li>'
    response += '</ul>'
    return HttpResponse(response)