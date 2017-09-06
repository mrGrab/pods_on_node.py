<H3> Nagios plugin for openshift </h3>

This is simple python script which sends api request to openshift (or kubernetes) master server: `/api/v1/pods` and parse json response.
<pre>
usage:
	 pods_on_node.py --ulr openshift_master --node node_name --token bearer_token 
	                  --warn int_of_pods --crit int_of_pods

Nagios plugin to get number of pods in node

optional arguments:
  -h, --help               show this help message and exit
  -u URL, --url URL        url:[port] of openshfit or kubernetes master server
  -n NODE, --node NODE     node name for which you need info
  -t TOKEN,--token TOKEN  token for connection to openshift master
  -w WARN, --warn WARN     warning level of quantity pods
  -c CRIT, --crit CRIT     critical level of quantity pods
</pre>
to use it you have to get token from secret for service account with cluster-reader permissions. If you have configured origin-metrics you can use heapster token:
<pre>
$ oc describe serviceaccount heapster -n openshift-infra

$ oc describe secret heapster-token-vs065
Name:		heapster-token-vs065
Namespace:	openshift-infra
Labels:		<none>
Annotations:	.....

Type:	kubernetes.io/service-account-token

Data
====
token:		HERE IS TOKEN

....
</pre>

but also you can create new one for nagios:
<pre>
$ oc create -f - << API
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nagios
secrets:
- name: nagios
API

$ oc describe serviceaccount nagios
$ oc describe secret nagios-token-zzzzz

oadm policy add-cluster-role-to-user cluster-reader system:serviceaccount:openshift-infra:nagios
</pre>

That's it. Enjoy.
