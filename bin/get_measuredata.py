import requests

URL = 'http://mickey.buaa.edu.cn:11401/condor/measurementdata/'
TOOL_NAME = ['IPERF', 'NETCAT', 'SCP', 'FDT']

parameters = {
	'source': 'murpa.rocksclusters.org',
	'destination': 'komatsu.chtc.wisc.edu',
	'timeEnd-start': '1447171200',			# 2015.11.11 00:00:00
	'timeEnd-end': '1447257600',			# 2015.11.12 00:00:00
	'tool_name': TOOL_NAME[0],
	'format': 'json',
}

data = requests.get(URL, params=parameters).json()

print(data)
