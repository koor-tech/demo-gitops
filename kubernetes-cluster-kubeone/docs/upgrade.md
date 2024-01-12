## How to do an upgrade for your koor storage distribution?

The steps are similar to rook/koor upgrade guide for our demo environment.

### Add helm chart repo

```console
$ helm repo add koor-release https://charts.koor.io/release
$ helm repo update
```

### Upgrade helm chart

```console
$ helm upgrade -nkoor-ceph koor-ceph-cluster koor-release/rook-ceph-cluster --set image.tag=v1.x.x (eg. v1.12.0)
```

For verification and upgrade for other components please refer [here](https://docs.koor.tech/v1.12/Upgrade/health-verification/).
