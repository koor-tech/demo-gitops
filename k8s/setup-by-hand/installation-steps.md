# Steps for Setting Up K8s and Ceph by Hand

We are setting up K8s and Ceph clusters. By following these steps, you should end up with a functioning K8s cluster and Ceph cluster. Will we use KSD or Rook to set up the Ceph cluster? Or will we create the Ceph cluster independently, and then use KSD to bring it into K8s?

Let's find out. But first, let's provision some hosts and get K8s running.

> In the interest of making progress, this will be neither perfect nor complete. Ask when anything is unclear or leaves too much to the imagination? In short, ask for help before you struggle too much.

## Provision and set up hosts

We are provisioning on [Hetzner cloud](https://www.hetzner.com/cloud), low costs virtual servers that we rent by the hour. Easy to set up and tear down. Plus, we can attach as much storage as we like.

Log in to one of our accounts to provision the hosts. If you work for Koor, ask someone how to get access.

In this case, we will set up 1 data control node (host). A high-availability setup would require at least 3 nodes. For data nodes, we can try different numbers of instances. We recommend 4 nodes for production, so it would be reasonable to do that for our standard demo system setup.

However, we can adjust things depending on what we are trying to show. The Ceph documentation talks about a 3-node minimum. We know that running only 3 nodes is risky -- problems happen when you lose one, even temporarily (from a networking issue or whatever). If we are just showing off some features of Koor software, we could get by with 3 nodes.

One experiment we can run is to see how few we can get away with and what happens at that level. Maybe we have have one larger host with 3 or more drives, giving us 3 or more OSD (one per drive). That could be cheaper to run, despite the risky business of having a single point of failure for our data cluster.

For these instructions, I will explain how to set up a control plane node, as well as a data storage node. The first part is the same for both.

### Set up non-root user with SSH access

We will set up a regular user to access the hosts. We will also want su privilege for system level actions, but otherwise, normal privilege is better.

- Create an SSH key from the Hetzner web interface.
- Set up SSH on your local machine
  - Put the private and public keys under .ssh
- Create your own private/public key pair - use protocol ed25519 or better
- Do this, replacing anything in angle brackets <> with actual values.

```bash
ssh root@<server_address>
adduser <newuser>
usermod -aG sudo newuser
mkdir ~/.ssh
vim ~/.ssh/authorized_keys
```

- Paste your SSH public key in the authorized_keys file. Save and close.
- From another terminal, ssh as the user you just set up.
- To make things easier, put a file called `config` in .ssh of your local machine. It will have entries like this:

```
Host <alias>
  HostName <ip address>
  User <user>
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_ed25519
```

- About config:
  - The alias can be anything easy to type. Has to be unique for each entry in this file.
  - Your identity file may be different. Regardless, point to the private key. The public key is on the remote server.

Do this for each server you provisioned. You'll want an easy way to access them all.

I like using a naming convention for the aliases. Starting with a common root, like 'demo-', I append 'cp' for control plane nodes, 'data' for data storage nodes. Number each one to make them unique.

For example, demo-cp1, demo-data1, demo-data2...

You might set the hostnames to match - that would be reassuring.

### Update everything

I installed Ubuntu 22.04. Whatever you installed, you'll want to make sure everything is up to date.

```bash
sudo update && sudo upgrade -y
```

When that's over, you may need to reboot the system for important changes to take effect. Do this:

```bash
sudo shutdown -r now
```

That will kick you out of your session because the server is rebooting. Won't take but a few seconds. Count to 10, and ssh back in.
