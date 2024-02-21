# Knative ML integration

Idea: 
- function triggered with S3 events when files are uploaded to input bucket, 
- does some machine learning transformation
- then outputs the files to output bucket

## Install rook-ceph
```bash
helm repo add rook-release https://charts.rook.io/release
helm repo update
helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph 
helm install --namespace rook-ceph rook-ceph-cluster \
   --set operatorNamespace=rook-ceph rook-release/rook-ceph-cluster

kubectl rook-ceph ceph status
```

## Install knative operator
```bash
kubectl apply -f deploy/operator.yaml
kubectl apply -f deploy/serving.yaml
kubectl patch service/kourier \
    -n knative-serving \
    --type merge -p '{"metadata": {"annotations": {"load-balancer.hetzner.cloud/name": "koor-demo-staging-kourier" }}}'
kubectl apply -f deploy/eventing.yaml

```

### Check deployment
```console
$ kubectl get deployment -n knative-eventing
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
ceph-controller         1/1     1            1           44s
ceph-webhook            1/1     1            1           43s
eventing-controller     1/1     1            1           3m5s
eventing-webhook        1/1     1            1           3m5s
imc-controller          1/1     1            1           3m1s
imc-dispatcher          1/1     1            1           3m
mt-broker-controller    1/1     1            1           2m58s
mt-broker-filter        1/1     1            1           2m59s
mt-broker-ingress       1/1     1            1           2m59s
pingsource-mt-adapter   0/0     0            0           3m5s
$ kubectl get KnativeEventing knative-eventing -n knative-eventing
NAME               VERSION   READY   REASON
knative-eventing   1.11.5    True    
```

## Install knative func
```bash
wget -O kn-func https://github.com/knative/func/releases/download/knative-v1.12.0/func_$(go env GOOS)_$(go env GOARCH)
chmod +x kn-func 
sudo mv kn-func /usr/local/bin
kn func version
```

## Install s5cmd
```bash
brew install peak/tap/s5cmd
```

## Create bucket claim
```console
$ kubectl apply -f deploy/obc.yaml 
$ kubectl describe objectbucketclaims.objectbucket.io
Name:         knative-ml-inputs
Namespace:    default
...
Spec:
  Bucket Name:           ml-inputs-9f6e8659-7bb5-4534-8579-9930ac8236dd
  Generate Bucket Name:  ml-inputs
  Object Bucket Name:    obc-default-knative-ml-inputs
  Storage Class Name:    ceph-bucket
Status:
  Phase:  Bound
Events:   <none>
```

## Add ceph source and notifications
```bash
kubectl apply -f deploy/notifications.yaml
kubectl apply -f deploy/ceph-source.yaml
kubectl apply -f deploy/trigger.yaml
```

## Create kantive function
```console
$ kn func create -l python ml
Created python function in /path/to/ml
$ tree ml -a
ml
├── app.sh
├── .func
├── .funcignore
├── func.py
├── func.yaml
├── .gitignore
├── Procfile
├── README.md
├── requirements.txt
└── test_func.py
```

## Add configmaps and secrets to func
Follow the prompts
```console
$ cd ml
$ kn func config env add
? What type of Environment variable do you want to add? ConfigMap: all key=value pairs as environment variables
? Which ConfigMap do you want to use? knative-ml-inputs
Environment variable entry was added to the function configuration
$ kn func config env add
? Where do you want to add the Environment variable? Insert here.
? What type of Environment variable do you want to add? Secret: all key=value pairs as environment variables
? Which Secret do you want to use? knative-ml-inputs
Environment variable entry was added to the function configuration
$ kn func config env
Configured Environment variables:
 -  All key=value pairs from ConfigMap "knative-ml-inputs"
 -  All key=value pairs from Secret "knative-ml-inputs"
```

This adds the following to func.yaml
```yaml
run:
  envs:
  - name: INPUTS_BUCKET_HOST
    value: '{{ configMap:knative-ml-inputs:BUCKET_HOST }}'
  - name: INPUTS_BUCKET_PORT
    value: '{{ configMap:knative-ml-inputs:BUCKET_PORT }}'
  - name: INPUTS_BUCKET_NAME
    value: '{{ configMap:knative-ml-inputs:BUCKET_NAME }}'
  - name: INPUTS_ACCESS_KEY_ID
    value: '{{ configMap:knative-ml-inputs:AWS_ACCESS_KEY_ID }}'
  - name: INPUTS_SECRET_ACCESS_KEY
    value: '{{ configMap:knative-ml-inputs:AWS_SECRET_ACCESS_KEY }}'
  - name: OUTPUTS_BUCKET_HOST
    value: '{{ configMap:knative-ml-outputs:BUCKET_HOST }}'
  - name: OUTPUTS_BUCKET_PORT
    value: '{{ configMap:knative-ml-outputs:BUCKET_PORT }}'
  - name: OUTPUTS_BUCKET_NAME
    value: '{{ configMap:knative-ml-outputs:BUCKET_NAME }}'
  - name: OUTPUTS_ACCESS_KEY_ID
    value: '{{ configMap:knative-ml-outputs:AWS_ACCESS_KEY_ID }}'
  - name: OUTPUTS_SECRET_ACCESS_KEY
    value: '{{ configMap:knative-ml-outputs:AWS_SECRET_ACCESS_KEY }}'
```


## Fill in code
...

## Build and push kantive function
```bash
cd ml
kn func build --registry docker.io/<your_username>
kn func deploy
```

## Configure external bucket access
```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.1 \
  --set installCRDs=true
```


```bash
kubectl apply -f deploy/ingress.yaml
export S3_ENDPOINT_URL=https://demo-staging.koor.dev

export INPUTS_BUCKET_NAME=$(kubectl -n default get cm knative-ml-inputs -o jsonpath='{.data.BUCKET_NAME}')
export INPUTS_ACCESS_KEY_ID=$(kubectl -n default get secret knative-ml-inputs -o jsonpath='{.data.AWS_ACCESS_KEY_ID}' | base64 --decode)
export INPUTS_SECRET_ACCESS_KEY=$(kubectl -n default get secret knative-ml-inputs -o jsonpath='{.data.AWS_SECRET_ACCESS_KEY}' | base64 --decode)

export OUTPUTS_BUCKET_NAME=$(kubectl -n default get cm knative-ml-outputs -o jsonpath='{.data.BUCKET_NAME}')
export OUTPUTS_ACCESS_KEY_ID=$(kubectl -n default get secret knative-ml-outputs -o jsonpath='{.data.AWS_ACCESS_KEY_ID}' | base64 --decode)
export OUTPUTS_SECRET_ACCESS_KEY=$(kubectl -n default get secret knative-ml-outputs -o jsonpath='{.data.AWS_SECRET_ACCESS_KEY}' | base64 --decode)

mkdir ~/.aws
cat > ~/.aws/credentials << EOF
[inputs]
aws_access_key_id = ${INPUTS_ACCESS_KEY_ID}
aws_secret_access_key = ${INPUTS_SECRET_ACCESS_KEY}

[outputs]
aws_access_key_id = ${OUTPUTS_ACCESS_KEY_ID}
aws_secret_access_key = ${OUTPUTS_SECRET_ACCESS_KEY}
EOF
```

## Invoke function
```bash
# upload
s5cmd --profile inputs cp input-imgs/pexels-justin-shaifer.jpg s3://$INPUTS_BUCKET_NAME
# list
s5cmd --profile inputs ls s3://$INPUTS_BUCKET_NAME
s5cmd --profile outputs ls s3://$OUTPUTS_BUCKET_NAME
#download
s5cmd --profile outputs cp s3://$OUTPUTS_BUCKET_NAME/pexels-justin-shaifer.jpg output-imgs/
```

## Check progress
```console
$ k logs -f ml-00003-deployment-5df4cdbbdf-cfs9t 
...
Loading pipeline components...: 100%|██████████| 6/6 [00:00<00:00,  9.07it/s], 364MB/s]
Key is pexels-justin-shaifer.jpgors:  99%|█████████▉| 3.40G/3.44G [00:09<00:00, 364MB/s]
Read input image
Input image size is (640, 427)
100%|██████████| 10/10 [00:56<00:00,  5.61s/it]
Write output image
Output image size (640, 424)
File is uploaded
```
