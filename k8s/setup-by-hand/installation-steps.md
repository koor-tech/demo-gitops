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

### Install dependencies and set up environment

_Note: you might want to ssh as root for the next bit of setup. That way, you won't need to keep typing `sudo`._

These instructions come from the setup for a Linux K8s class:

`sudo apt install curl apt-transport-https vim git wget software-properties-common lsb-release ca-certificates -y`

An up-to-date Ubuntu 22.04 says only `apt-transport-https` was new. Everything else was already up to date. That means this should be sufficient.

`sudo apt install apt-transport-https -y`

Now disable swap and load modules

```bash
sudo swapoff -a
sudo modprobe overlay
sudo modprobe br_netfilter
```

**Update kernel networking**

Two ways to do this.

...this will work in a script and at the command line

```bash
root@cp:˜# cat << EOF | tee /etc/sysctl.d/kubernetes.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
```

OR just create a file...

`sudo vi /etc/sysctl.d/kubernetes.conf`

...and paste in the lines

```
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
```

Ensure the changes are made:

`sysctl --system`

### Name the machines

```
root@demo-cp1:~# hostname -i
127.0.1.1

root@demo-cp1:~# ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
link/ether 96:00:02:99:67:5e brd ff:ff:ff:ff:ff:ff
inet 5.78.105.125/32 metric 100 scope global dynamic eth0
valid_lft 45766sec preferred_lft 45766sec
inet6 2a01:4ff:1f0:e30b::1/64 scope global
valid_lft forever preferred_lft forever
inet6 fe80::9400:2ff:fe99:675e/64 scope link
valid_lft forever preferred_lft forever
3: enp7s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq_codel state UP group default qlen 1000
link/ether 86:00:00:5f:c8:7e brd ff:ff:ff:ff:ff:ff
inet 10.0.0.2/32 brd 10.0.0.2 scope global dynamic enp7s0
valid_lft 86093sec preferred_lft 86093sec
inet6 fe80::8400:ff:fe5f:c87e/64 scope link
valid_lft forever preferred_lft forever
```

### Install containerd or CRI-O, not both

Clearly containerd is better, except CRI-O is better for different reasons. Why not use one or the other? Why not? For all of the "purity" of CRI-O, it's based on Debian libraries that are not signed, maybe not even kept up. Meh.

#### CRI-O (not a happy path)

(This does not end well, but you can see the instructions I found. Maybe there's a better source.)

We will try CRI-O first because it's "better suited for Kubernetes" and people seem to want to run from Docker.

Following the instructions in the [CRI-O repo](https://github.com/cri-o/cri-o/blob/main/install.md).

To install on apt-based system, like Ubuntu, set an environment variable ([other flavors found here](https://github.com/cri-o/cri-o/blob/main/install.md#apt-based-operating-systems))

`export OS=xUbuntu_22.04`

Then keep following along. Install cri-o-runc, which needs libseccomp >= 2.4.1

There's a problem getting a Debian library from backports due to lack of signature. Everything stops at that point. So close...

!!!! WAAAA - DEAD END !!!!

If you don't go any further with CRI-O, delete any files you created before hitting the dead end. Otherwise, you will not be able to install anything else.

#### containerd (happier path)

Set up key for software install.

```bash
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install

```bash
apt-get update && apt-get install containerd.io -y
containerd config default | tee /etc/containerd/config.toml
sed -e 's/SystemdCgroup = false/SystemdCgroup = true/g' -i /etc/containerd/config.toml
systemctl restart containerd
```

It works! Come on. How is that not better?

#### Configuring the systemd cgroup driver

There is a lot of talk about this in the instructions. For me, it was configured correctly by default. No change required.

## Install k8s things: kubeadm, kubelet, kubectl

Get keys:

`curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg`

Install and prevent automatic upgrades:

```bash
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

## Initializing control plane node

- Recommendation if planning to upgrade to HA -- which I am not
- Suggested to add Pod network add-on and see if necessary to set --pod-network-cidr

`kubeadm init <args>`

And that's it. Really? args? Just read the [reference manual](https://kubernetes.io/docs/reference/setup-tools/kubeadm/). Or use a file, and there's a manual for that, too.

Ridiculous.

### No wait. I found better instructions

From the course material.

`vi kubeadm-config.yaml`

Paste in this:

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: 1.27.1 #<-- Use the word stable for newest version
controlPlaneEndpoint: "k8scp:6443" #<-- Use the alias we put in /etc/hosts not the IP
networking:
  podSubnet: 192.168.0.0/16 #<-- Match the IP range from the CNI config file
```

Initialize with:

`kubeadm init --config=kubeadm-config.yaml --upload-certs | tee kubeadm-init.out`

A lot of stuff happens. When it's over, that's the time to deploy a pod network.

For reference:

```
To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of the control-plane node running the following command on each as root:

  kubeadm join demo-cp1:6443 --token qmnqa1.yzgire0kumdy1kbw \
  --discovery-token-ca-cert-hash sha256:c887b75c3ce657feeb62e0fe3021d237ac182538bf2231e419bc80e076e08616 \
  --control-plane --certificate-key 56a9c57464f1b36989ec699a0dedfe54d7ad8eb3dd0b12ba2b3f208d03f1e869

Please note that the certificate-key gives access to cluster sensitive data, keep it secret!
As a safeguard, uploaded-certs will be deleted in two hours; If necessary, you can use
"kubeadm init phase upload-certs --upload-certs" to reload certs afterward.

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join demo-cp1:6443 --token qmnqa1.yzgire0kumdy1kbw \
  --discovery-token-ca-cert-hash sha256:c887b75c3ce657feeb62e0fe3021d237ac182538bf2231e419bc80e076e08616
```

## Installing a pod network add-on

We need a Container Network Interface (CNI) for the pods to communicate with each other. I'm going to use Cilium. Other options could work too. The demo system is using Calico (at the time of writing), and Multus can make sense.

### Cilium installation

Install CLI

```bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
```

Now install Cilium...but it's not working

`cilium install --version 1.14.2`

Troubleshooting

From [somebody's Medium blog](https://akyriako.medium.com/install-kubernetes-1-27-with-cilium-on-ubuntu-16193c7c2ac6):

enable CRI plugins
`sudo sed -i 's/^disabled_plugins \=/\#disabled_plugins \=/g' /etc/containerd/config.toml`

install CNI plugins

```
sudo mkdir -p /opt/cni/bin/
sudo wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz
```

enable and restart the containerd service:

```
systemctl enable containerd
systemctl restart containerd
```

As second step we need to configure our linux boxes to forward IPv4 and instruct iptables to see bridged traffic:

```
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```
