#!/usr/bin/python

from influxdb import InfluxDBClient
import psutil
import time
import fritzconnection as fc
import json

config = json.loads(open('config.json').read())

db = InfluxDBClient(config['influx']['host'], 
		    config['influx']['port'], 
		    config['influx']['user'], 
		    config['influx']['pw'], 
		    config['influx']['db'])
fbstatus = fc.FritzStatus(address=config['fritzbox']['address'], port=config['fritzbox']['port'])
hostname = config['hostname']

def log_cpu():
	db.write_points([{
    		"name": "cpu_idle",
    		"columns": ["value", "host"],
    		"points": [
        		[psutil.cpu_percent(interval=1), hostname]
    		]
	}])

def log_mem():
	mem = psutil.virtual_memory()
	db.write_points([{
    		"name": "mem_usage",
    		"columns": ["used", "total", "percent", "host"],
    		"points": [
        		[mem.used, mem.total, mem.percent, hostname]
    		]
	}])

def log_uplink():
	upstream, downstream = fbstatus.transmission_rate
	db.write_points([{
    		"name": "uplink_usage",
    		"columns": ["upstream", "downstream"],
    		"points": [
        		[upstream, downstream]
    		]
	}])

while True:
	log_cpu()
	log_mem()
	log_uplink()
	time.sleep(1)

