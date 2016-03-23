#!/usr/bin/python
#coding: UTF-8

import requests, sys, argparse

parser = argparse.ArgumentParser(prog='pods_on_node.py', usage='\n\t %(prog)s --ulr <openshift_master> --node <node_name> --token <bearer_token> --warn <int_of_pods> --crit <int_of_pods>', description='Nagios plugin to get quantity of pods in node', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30))
parser.add_argument('-u','--url', action='store',  help="url:[port] of openshfit or kubernetes master server", required=True)
parser.add_argument('-n','--node', action='store', help="node name for which you need info", required=True)
parser.add_argument('-t','--token', action='store', help="token for connection to openshift master", required=True)
parser.add_argument('-w','--warn', type=int, action='store', help="warning level of quantity pods", required=True)
parser.add_argument('-c','--crit', type=int, action='store', help="critical level of quantity pods", required=True)
args = parser.parse_args()

headers = {'Authorization': 'Bearer '+args.token}
params={'fieldSelector': 'spec.host='+args.node}

try:
	req = requests.get(args.url+"/api/v1/pods", verify=False, headers=headers, params=params)
	if req.status_code <> 200: raise Exception()
except BaseException:
	print "UKNOWN - can't connect to server or wrong http response"
	sys.exit(3)

pods = len(req.json()['items'])
if pods < args.warn:
	print "OK - running %s pod(s)." % pods
	sys.exit(0)
elif pods >= args.warn and pods < args.crit:
	print "WARNING - running %s pod(s)." % pods
        sys.exit(1)
elif pods >= args.crit:
	print "CRITICAL - running %s pod(s)." % pods
	sys.exit(2)
else:
	print "UKNOWN - running %s pod(s)." % pods
	sys.exit(3)


