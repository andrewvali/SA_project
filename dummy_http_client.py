import http.client
import json

conn = http.client.HTTPConnection('localhost:8000')

headers = {'Content-type': 'application/json'}

#CHOOSE YOUR QUERY BY COMMENTING AND UNCOMMENTING
post_query = {'type': 'event per ship',
              'query':{ 'vessel':'ves227443000','event':'GapEnd'}}

#post_query = {'type': 'interdiction area', 'query':{ 'vessel':'all'}}

#post_query = {'type': 'protected area',
#              'query':{ 'vessel':'all','event':'all','protectedArea':'natura_FR5302006'}}

json_data = json.dumps(post_query)

conn.request('POST', '/post', json_data, headers)

response = conn.getresponse()
result_query = json.loads(response.read().decode()) #RETURNS QUERY RESULT AS A DICT
print(result_query)