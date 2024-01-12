# How to use Flux CD for Koor and Rook deployments

Flux CD enables GitOps-style deployment for Kubernetes clusters by automating application and infrastructure deployment using Git repositories. It uses YAML manifests stored in a Git repository to define the desired state of the cluster. Flux CD continuously monitors the repository for changes and applies them to the cluster, ensuring consistency. It provides standardized and auditable deployment processes, promotes collaboration and version control, and allows for automated rollouts and integration with CI/CD pipelines. With Flux CD, you can streamline and automate the deployment process for your Kubernetes applications and infrastructure.

For more information, you can refer to the official Flux CD documentation [here](https://fluxcd.io/docs/).

## **Installing Koor Ceph cluster**

## **Before you begin**

To follow the guide, you need the following:

- **A Kubernetes cluster**. We recommend [Kubernetes kind](https://kind.sigs.k8s.io/docs/user/quick-start/) for trying Flux out in a local development environment.
- **A GitHub personal access token with repo permissions for demo-gitops repo**. See the GitHub documentation on [creating a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) or ask your Koor admin.

## **Installation Guide**

Installation is pretty straightforward, you have to pull demo-gitops repository to your dev environment, for dev environment setup, we are testing this on a 3 node minikube cluster, for demo environment please skip this step

`$ minikube start --disk-size=40g --extra-disks=2 --driver kvm2 --nodes 3`

Clone the demo-gitops repository

```console
$ git clone <https://github.com/koor-tech/demo-gitops>
```

Make sure you have the right Kubernetes cluster context available. After ensuring the right cluster to install koor-ceph cluster, run the following command:

```console
$ flux bootstrap github \
--owner=koor-tech \
--repository=demo-gitops \
--branch=main \
--path=./flux \
--personal --token-auth --read-write-key --verbose

```

Note: You would require GitHub token with the right repo permissions for this step. Please check the before-installation step.

At this point Flux installs and configures the cluster for you, you should be able to checkout installed resources and their state using following commands

```console
$ flux get kustomizations koor-ceph
$ flux get helmreleases -n koor-ceph koor-release
```

You should be able to see operator installation as well as cluster installation success using kubectl commands:

```console
flux-system   helm-controller-7b5c885fb5-njpjs                            1/1     Running            0             9m4s
flux-system   kustomize-controller-746fdf87bf-glstw                       1/1     Running            0             9m4s
flux-system   notification-controller-5646f6df46-cjvrb                    1/1     Running            0             9m3s
flux-system   source-controller-64484988c4-sq758                          1/1     Running            0             9m3s
koor-ceph     rook-ceph-operator-7f9fcb6c56-lp7mb                         0/1     ImagePullBackOff   0             8m46s
```

For troubleshooting, these command help check a resource's status and flux logs associated with deployment.

```console
$ flux logs
$ flux get helmreleases -n koor-ceph koor-release
```

To install koor-ceph the gitops way, we will begin by exploring how the structure of the repository has been configured

cheatsheet for flux commonly used commands

```console
$ flux get kustomizations rook-ceph
$ flux get helmreleases -n rook-ceph rook-ceph
```

Note: For demo system users Koor to have the gitops repo access, to make changes to the flux scripts you should have access to push into the koor demo-gitops repository.
