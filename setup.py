import yaml
import distutils.spawn
import json
import os
import pathlib
from subprocess import check_call,check_output
from sys import exit
from time import sleep

"""
regions = {
    'region': 'kubectl context'
}
"""
regions = {
    'europe-west4': 'gke_PROJECT_ID_REGION_CLUSTER'
}

# region: [zones]
zones = {
    'europe-west4': ['europe-west4-a', 'europe-west4-b', 'europe-west4-c']
}

for region, context in regions.items():
    try:
        check_call(['kubectl', 'get', 'pods', '--context', context])
    except:
        exit("unable to make basic API call using kubectl context '%s' for cluster in zone '%s'; please check if the context is correct and your Kubernetes cluster is working" % (context, region))

for region, context in regions.items():
    region_zones = ", ".join(zones[region])
    with open("storageclass_zeebe_template.txt", 'r') as storageclass:
        doc = yaml.load(storageclass.read(), Loader=yaml.SafeLoader)
        doc["parameters"]["zones"] = region_zones
        with open("03_storageclass_zeebe.yml", "w") as region_storageclass:
            region_storageclass.write(yaml.dump(doc))
    for yml in sorted(list(pathlib.Path('.').glob('*.yml'))):
        check_call(['kubectl', 'apply', '-f', yml, '--context', context])
  