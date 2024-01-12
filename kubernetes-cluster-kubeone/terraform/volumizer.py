import os
import sys
import getopt
import re

import hcloud

expression = re.compile('pool', re.IGNORECASE)


def create_and_associate_volume(client, worker, size):
    try:
        response = client.volumes.create(size=size, name=f"${worker.name}-vol-1")
    except hcloud.APIException:
        raise
    volume = response.volume
    volume.attach(worker)



def parseOpts():
    args = sys.argv[1:]
    size = 10
    name = "koor-generic"
    try: 
        opts, args = getopt.getopt(args, 's:h', ["size=", "help"])
    except getopt.GetoptError:
        print('Usage: volumizer.py --size <size in gigabytes>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage: volumizer.py --size <size in gigabytes>')
            sys.exit()
        if opt in ("-s", "--size"):
            size = int(arg)
    
    return size


if __name__ == "__main__":
    assert (
        "HCLOUD_TOKEN" in os.environ
    ), "Please export your API token in the HCLOUD_TOKEN environment variable"
    token = os.environ["HCLOUD_TOKEN"]
    client = hcloud.Client(token=token)

    size = parseOpts()

    try:
        servers = client.servers.get_all()
    except hcloud.APIException:
        raise

    for i in range(len(servers)):
        if expression.search(servers[i].name):
            if not servers[i].volumes:
                print(f"No volumes attached to ${servers[i].name}.  Creating and associating.")
                create_and_associate_volume(client=client, worker=servers[i], size=size)



    
    

