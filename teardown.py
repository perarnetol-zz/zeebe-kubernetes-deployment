import pathlib 
from shutil import rmtree
from subprocess import call

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
    for yml in sorted(list(pathlib.Path('.').glob('*.yml')), reverse=True):
        call(['kubectl', 'delete', '-f', yml, '--context', context])
