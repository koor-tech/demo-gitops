---
title: Configuring Ingress for Koor Data Control Center Dashboard and Ceph Dashboard
---

# Installing Koor Data Control Center

This document contains the steps necessary to install Koor Data Control Center on the demo envireonment.

## Install Cert-Manager and Let's Encrypt Issuers

This allows creating a TLS certificate for the cluster

1. Add the Helm repository

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

2. Install `cert-manager`

```bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.1 \
  --set installCRDs=true
```

3. Add Let's Encypt issuers

```bash
kubectl apply -f issuers.yaml
```

::: code-group
```yaml [issuers.yaml]
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-prod
  namespace: koor-ceph
spec:
  acme:
    # The ACME server URL
    server: https://acme-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: admin@koor.tech
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
      - http01:
          ingress:
            ingressClassName: nginx
```
:::

References: 
1. https://cert-manager.io/docs/installation/helm/
2. https://cert-manager.io/docs/tutorials/getting-started-with-cert-manager-on-google-kubernetes-engine-using-lets-encrypt-for-ingress-ssl/

## Install Nginx Ingress and a Load Balancer

1. Create a Load Balancer in Hetzner. Choose the network of the cluster. 
Remove all targets and services since they will be added automatically. 
Name your load balancer `demolb`

2. Install ingress-nginx using the helm chart

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm -n ingress-nginx install ingress-nginx ingress-nginx/ingress-nginx --create-namespace -f nginx-values.yaml
```

::: code-group
```yaml [nginx-values.yaml]
controller:
  config:
    entries:
        use-forwarded-headers: "true"
        compute-full-forwarded-for: "true"
        use-proxy-protocol: "true"
  service:
    annotations:
      # This is the name of the load balancer just created
      load-balancer.hetzner.cloud/name: "demolb"
```
:::

References:
1. https://community.hetzner.com/tutorials/howto-k8s-authentication-with-load-balancer
2. https://kubernetes.github.io/ingress-nginx/deploy/#ovhcloud

## Install Koor Data Control Center and Enable Ingress
Finally we are ready to install KDCC using [the helm chart](https://github.com/koor-tech/data-control-center/tree/main/charts/data-control-center).

```bash
helm repo add data-control-center https://koor-tech.github.io/data-control-center
helm repo update
helm install --create-namespace --namespace rook-ceph data-control-center data-control-center/data-control-center -f values.yaml
```

::: code-group
```yaml [values.yaml]
config:
  users:
    - username: admin
      password: "<SomeStrongPassword>"
```
:::

## Create a DNS entry for the demo system

Add the following to the `infra` repository, we add names we will be using as
CNAMES, the ngnix ingress will handle routing the traffic based on subdomain
name. See more (here)[https://kubernetes.io/docs/concepts/services-networking/ingress/#name-based-virtual-hosting]

```js
  A("k8s-lb", "<Load balancer IPv4>"),
  AAAA("k8s-lb", "<Load balancer IPv6>"),
  CNAME("demo", "k8s-lb"),
  CNAME("ceph", "k8s-lb"),
```

## Setup 

::: code-group
```yaml [data-control-center-ingress.yaml]
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: koor-dashboard-demo
  namespace: rook-ceph # namespace:cluster
  annotations:
    cert-manager.io/issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: "nginx"
  tls:
    - hosts:
        - demo.koor.tech
      secretName: koor-dashboard-demo-secret-data
  rules:
    - host: demo.koor.tech
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: data-control-center
                port:
                  number: 8282

```
:::

Apply the yaml and verify if everything is configured fine.

```console
kubectl create -f data-control-center-ingress.yaml
```

## Setup Ceph Dashboard Ingress

Similarly, configure hostname for ceph dashboard in this example yaml.

::: code-group
```yaml [dashboard-ingress-https.yaml]
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: koor-dashboard-demo-ceph
  namespace: rook-ceph # namespace:cluster
  annotations:
    cert-manager.io/issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/server-snippet: |
      proxy_ssl_verify off;
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: "nginx"
  tls:
    - hosts:
        - ceph.koor.tech
      secretName: ceph-demo-secret
  rules:
    - host: ceph.koor.tech
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rook-ceph-mgr-dashboard
                port:
                  name: https-dashboard
```
:::

```console
kubectl create -f dashboard-ingress-https.yaml
```

## Validate that the Ingress is running 

```console
$ kubectl get -n koor-ceph ingress
NAME                  CLASS   HOSTS            ADDRESS                                           PORTS     AGE
data-control-center   nginx   demo.koor.tech   <Load balancer IPv4>,192.168.0.x,<Load balancer IPv46>   80, 443   12h
koor-dashboard-demo-ceph   nginx   ceph.koor.tech <Load balancer IPv4>,192.168.0.x,<Load balancer IPv46>   80, 443   22h
```
