# Knative integration

## Install knative operator
```bash
kubectl apply -f operator.yaml
kubectl apply -f serving.yaml

```

## Install knative func
```bash
wget -O kn-func https://github.com/knative/func/releases/download/knative-v1.12.0/func_$(go env GOOS)_$(go env GOARCH)
chmod +x kn-func 
sudo mv kn-func /usr/local/bin
kn func version
```

## Create kantive function
```bash
kn func create -l go hello
cd hello
kn func build --registry docker.io/<your_registry>
kn func run
kn func deploy
kn func invoke
```