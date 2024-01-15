#!/usr/bin/python3

########
#
# volumizer.py, the simple and effective way of adding volumes to your cluster!
# 
# usage: ./volumizer.py -c <cluster name> -s <size>
#
# Relies on the hcloud python library:
# $ pip3 install hcloud
#

import os
import argparse
import re

import hcloud

def create_and_associate_volume(client, worker, size):
    volumeName = f"{worker.name}-vol-1"
    try:
        print(f"Creating volume to Hetzner Cloud for {worker.name}.")
        response = client.volumes.create(size=size, name=volumeName, location=worker.datacenter)
    except hcloud.APIException:
        raise
    volume = response.volume
    volume.attach(worker)

def parseOpts():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--size", type=int, default=10, help="the size of each worker's volume, in gigabyes")
    parser.add_argument("-c", "--cluster-name", type=str, default="pool", help="the name of your cluster")

    args = parser.parse_args()
    return args.cluster_name, args.size

if __name__ == "__main__":
    assert (
        "HCLOUD_TOKEN" in os.environ
    ), "Please export your API token in the HCLOUD_TOKEN environment variable"
    token = os.environ["HCLOUD_TOKEN"]
    client = hcloud.Client(token=token)

    name, size = parseOpts()

    inCluster = re.compile(f'{name}', re.IGNORECASE)
    inPool = re.compile('pool', re.IGNORECASE)

    try:
        servers = client.servers.get_all()
    except hcloud.APIException:
        raise

    for i in range(len(servers)):
        if inCluster.search(servers[i].name) and inPool.search(servers[i].name):
            if not servers[i].volumes:
                print(f"There are no volumes attached to {servers[i].name}. Creating and associating.")
                create_and_associate_volume(client=client, worker=servers[i], size=size)
