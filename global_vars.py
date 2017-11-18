import os
import redis
from datetime import datetime

def init():
	global prefixes
	prefixes = ["RPMs","Load","Throttle","Coolant","O2","Speed","Gear","Volts","RRPot","RLPot"]

	global primaries
	primaries = ["RPMs","Load","Throttle","RRPot","RLPot"]

	global secondaries
	secondaries = ["Coolant","O2","Speed","Gear","Volts"]

	global data
	data = {prefix: 0 for prefix in prefixes}

	sep = "\\" if os.name == "nt" else "/"
	directory = os.getcwd()+sep+"logs"+sep+"Engine Data "+datetime.today().strftime('%m-%d-%Y')+" "+datetime.now().strftime('%H:%M:%S')+sep
	if not os.path.exists(directory):
		os.makedirs(directory)

	global filenames
	filenames = {prefix: directory+prefix+".csv" for prefix in prefixes}

	global database
	database = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)