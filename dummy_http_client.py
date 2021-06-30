import http.client
import json

#Client test script

conn = http.client.HTTPConnection('localhost:8000')
headers = {'Content-type': 'application/json'}

# SAMPLE POST REQUESTS JSON INPUT
# CHOOSE YOUR QUERY BY COMMENTING AND UNCOMMENTING
post_query = {'type': 'event per ship',
              'query':{ 'vessel':'ves227443000','event':'GapEnd',
                        'date1':'2015-09-30 22:00', 'date2':'2017-09-30 22:00'}}

#post_query = {'type': 'interdiction area',
#              'query':{ 'vessel':'all',
#                        'date1':'2015-09-30 22:00', 'date2':'2017-09-30 22:00'}}

#post_query = {'type': 'protected area',
#              'query':{ 'vessel':'all','event':'all','protectedArea':'natura_FR5302006',
#                        'date1':'2015-09-30 22:00', 'date2':'2017-09-30 22:00'}}


# COMMUNICATING TO SERVER
json_data = json.dumps(post_query)
conn.request('POST', '/post', json_data, headers)
response = conn.getresponse()
# RETURNS QUERY RESULT AS A DICT
result_query = json.loads(response.read().decode())
print(result_query)

