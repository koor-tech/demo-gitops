# Knative integration

Idea: 
- function triggered with S3 events when files are uploaded to input bucket, 
- does some machine learning transformation
- then outputs the files to output bucket

## Install knative operator
```bash
kubectl apply -f deploy/operator.yaml
kubectl apply -f deploy/serving.yaml
kubectl patch service/kourier \
    -n knative-serving \
    --type merge -p '{"metadata": {"annotations": {"load-balancer.hetzner.cloud/name": "koor-demo-staging-kourier" }}}'

```

## Install knative func
```bash
wget -O kn-func https://github.com/knative/func/releases/download/knative-v1.12.0/func_$(go env GOOS)_$(go env GOARCH)
chmod +x kn-func 
sudo mv kn-func /usr/local/bin
kn func version
```

## Create bucket claim

## Create kantive function
```bash
kn func create -l go ml
```

## Fill in code
...


## Add bc to funcs


## Build and push kantive function
```bash
cd producer
kn func build --registry docker.io/<your_username>
kn func deploy
```

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
