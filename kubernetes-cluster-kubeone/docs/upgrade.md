## How to do an upgrade for your koor storage distribution?

The steps are similar to rook/koor upgrade guide for our demo environment

### Upgrade helm chart

```code
$ helm upgrade -nkoor-ceph koor-ceph-cluster koor-release/rook-ceph-cluster --set image.tag=v1.x.x (eg. v1.12.0)
```

For verification and upgrade for other components please refer [here](https://docs.koor.tech/v1.12/Upgrade/health-verification/)

