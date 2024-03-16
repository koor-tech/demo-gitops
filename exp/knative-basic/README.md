# Knative integration

Idea: File buffer using producer and consumer
Producer creates files with random sizes. Limited to a number of files.
Consumer picks random file, calculates md5 and size then deletes the file, sends that to output.

This could be intermediate files in your image processing pipeline or [find applications]

## Install knative operator
```bash
kubectl apply -f deploy/operator.yaml
kubectl apply -f deploy/serving.yaml
```

## Install knative func
```bash
wget -O kn-func https://github.com/knative/func/releases/download/knative-v1.12.0/func_$(go env GOOS)_$(go env GOARCH)
chmod +x kn-func 
sudo mv kn-func /usr/local/bin
kn func version
```

## Create pvc
```bash
kubectl apply -f deploy/pvc.yaml
```

## Create kantive functions
```bash
kn func create -l go producer
kn func create -l go consumer
kn func create -l go list
```

## Fill in code
...

## Enable PVC usage and configure the functions to use the pvc
https://knative.dev/docs/serving/configuration/feature-flags/#kubernetes-persistentvolumeclaim-pvc

```yaml
    features:
      kubernetes.podspec-persistent-volume-claim: "enabled"
      kubernetes.podspec-persistent-volume-write: "enabled"
      kubernetes.podspec-securitycontext: "enabled"
```

## Add pvc to funcs
```bash
kn func config volumes add
```

or add this to `func.yaml`
```bash
run:
  volumes:
  - presistentVolumeClaim:
      claimName: knative-pc-cephfs
    path: /files
```

## Build and push kantive function
```bash
cd producer
kn func build --registry docker.io/<your_username>
kn func deploy

# this is to fix permission issues
kubectl patch services.serving/producer --type merge \
    -p '{"spec": {"template": {"spec": {"securityContext": {"fsGroup":1000}}}}}'
```
do the same for consumer.

## Invoke function
```console
$ kn func invoke
TODO result
```

## Undeploy function
```console
$ kn func delete consumer
Removing Knative Service: consumer
Removing Knative Service 'consumer' and all dependent resources
```
