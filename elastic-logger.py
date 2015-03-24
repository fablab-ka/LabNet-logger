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

es.indices.create(index='server-index', ignore=400)
es.indices.create(index='fritzbox-index', ignore=400)

def log_disk():
	partitions = psutil.disk_partitions()
	for p in partitions:
		disk = psutil.disk_usage(p.mountpoint)
		res = es.index(index="server-index", doc_type='disk', body={
    		"mount": p.mountpoint,
    		"used": disk.used,
    		"free": disk.free,
    		"percent": disk.percent,
    		"hostname": hostname,
    		"@timestamp": datetime.utcnow()
		})

def log_cpu():
	cpu = psutil.cpu_percent(interval=1)
	res = es.index(index="server-index", doc_type='cpu', body={
    	"value": cpu,
    	"@timestamp": datetime.utcnow()
	})
	print "CPU -> val:" + str(cpu)

def log_mem():
	mem = psutil.virtual_memory()
	res = es.index(index="server-index", doc_type='memory', body={
    	"used": mem.used/1024/1024,
    	"total": mem.total/1024/1024,
    	"percent": mem.percent,
    	"@timestamp": datetime.utcnow()
	})
	print "RAM -> used:" + str(mem.used/1024/1024) + "MB" 

def log_uplink():
	upstream, downstream = fbstatus.transmission_rate
	upstream = upstream/1024 #to kb
	downstream = downstream/1024 #to kb
	res = es.index(index="fritzbox-index", doc_type='traffic', body={
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
	log_disk()
	time.sleep(1)

