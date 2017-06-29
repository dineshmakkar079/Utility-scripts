import urllib.request
import os
import sys
import json
import time

if __name__ == "__main__":
	if(not len(sys.argv) == 2):
		print("Usage : python3  match.py MATCH_ID")
	else:
		matchid = sys.argv[1]
		while(True):
			state = ''
			try :
				res =  urllib.request.urlopen('http://push.cricbuzz.com/match-push?id='+str(matchid))
				jsonObj = json.loads(res.read().decode('utf-8'))
				message = jsonObj["score"]["batting"]["score"];
				state = jsonObj["state"]
				print(message)
				os.system("notify-send '" + message + "'");
				if(state == 'complete'):
					os.system("notify-send 'Match completed.'")
					break
				time.sleep(60)
			except Exception as e:
				print("Some error occured" + str(e))
				break
