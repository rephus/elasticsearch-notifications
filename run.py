#/bin/python
from services.gmail import Gmail
import ConfigParser
from datetime import datetime
from elasticsearch import Elasticsearch # http://elasticsearch-py.readthedocs.org/en/master/

config = ConfigParser.ConfigParser()
config.read("config.cfg")

user =config.get('gmail', 'user')
password =config.get('gmail', 'password')
email_to = [config.get('config','notification-email')]
gmail = Gmail(user,password)

es_endpoint = config.get('es', 'endpoint')
es_port =  config.get('es', 'port')
es_server = "{}:{}".format(es_endpoint,es_port)
es = Elasticsearch([es_server])

#List indices: curl localhost:9200/_cat/indices?v
index= config.get('es', 'index')
time_filter= config.get('es', 'time-filter')

print "Querying ES {} index {} with timeFilter {}".format(es_server,index,time_filter)
#es range filter: http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_ranges.html
search={
  "query":  {
    "filtered": {
      "filter": {
        "range": { "@timestamp": { "gt": time_filter} }
      }
    }
  },
  "size": 0,
  "aggs": {
        "group_by_user": {
          "terms": {
            "field": "email"
          }
        }
  }
}

res = es.search(index=index, body=search)

buckets = res['aggregations']['group_by_user']['buckets']
total = len(buckets)

if not total:
  print "No records"
else:
  print "Found {} users, sending email".format(total)
  print buckets

  title = "ES '{}' daily report".format(index)
  body =  """
Found {} users.

Buckets: {}
""".format(total,buckets )

  gmail.send(email_to, title, body)
