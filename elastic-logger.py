#!/usr/bin/python

import time
from datetime import datetime
from elasticsearch import Elasticsearch
import psutil
import time
import fritzconnection as fc
import json

es = Elasticsearch()
config = json.loads(open('config.json').read())

fbstatus = fc.FritzStatus(address=config['fritzbox']['address'], port=config['fritzbox']['port'])
hostname = config['hostname']

es.indices.create(index='fileserv-index', ignore=400)
es.indices.create(index='fritzbox-index', ignore=400)

def log_cpu():
	cpu = psutil.cpu_percent(interval=1)
	res = es.index(index="fileserv-index", doc_type='cpu', body={
    	"name": "cpu_idle",
    	"value": cpu,
    	"@timestamp": datetime.utcnow()
	})
	print "CPU -> val:" + str(cpu)

def log_mem():
	mem = psutil.virtual_memory()
	res = es.index(index="fileserv-index", doc_type='memory', body={
    	"name": "mem_usage",
    	"used": mem.used/1000000,
    	"total": mem.total/1000000,
    	"percent": mem.percent/1000000,
    	"@timestamp": datetime.utcnow()
	})
	print "RAM -> used:" + str(mem.used/1000000) + "MB" 

def log_uplink():
	upstream, downstream = fbstatus.transmission_rate
	upstream = upstream/1000 #to kb
	downstream = downstream/1000 #to kb
	res = es.index(index="fritzbox-index", doc_type='traffic', body={
    	"name": "traffic",
    	"upstream": upstream,
    	"downstream": downstream,
    	"@timestamp": datetime.utcnow()
	})
	print "FB -> up:" + str(upstream) + "kbps" 
	print "FB -> down:"  + str(downstream) + "kbps"

while True:
	print str(datetime.utcnow()) + " ==== " + str(time.time())
	log_cpu()
	log_mem()
	log_uplink()
	time.sleep(1)

