from django.shortcuts import render
from django.http import HttpResponse

import facebook as fb

version = '3.1'

# Create your views here.
def feed(request, access_token):
    graph = fb.GraphAPI(access_token=access_token, version=version)
    feed = graph.get_connections(id='me', connection_name='feed')
    response = '<ul>'
    response = []
    for post in feed['data']:
        response += '<li>'
        for key in post.keys():
            if key == 'id':
                response += "<a href='/facebook_benchmark/post/" + post.get(key, '') + "/" + access_token + "'>" + post.get(key, '') + "</a> "
            else:
                response += post.get(key, '') + ' '
        response += '</li>'
    response += '</ul>'
    return HttpResponse(response)

def post(request, id, access_token):
    graph = fb.GraphAPI(access_token=access_token, version=version)
    post = graph.get_object(id=id)
    response = '<ul><li>'
    for key in post.keys():
        response += post.get(key, '') + ' '
    response += '</li></ul>'
    return HttpResponse(response)