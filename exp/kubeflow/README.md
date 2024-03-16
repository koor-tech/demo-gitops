# Kubeflow with Ceph

## Tools
```bash
brew install argocd
brew install jq
```

## Install rook-ceph
```bash
helm repo add rook-release https://charts.rook.io/release
helm repo update
helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph 
helm install --namespace rook-ceph rook-ceph-cluster \
   --set operatorNamespace=rook-ceph rook-release/rook-ceph-cluster

kubectl rook-ceph ceph status
```

## Install argocd
```bash
# clone the deploykf repo
# NOTE: we use 'main', as the latest plugin version always lives there
git clone -b main https://github.com/deployKF/deployKF.git ./deploykf

# ensure the script is executable
chmod +x ./deploykf/argocd-plugin/install_argocd.sh

# run the install script
# WARNING: this will install into your current kubectl context
bash ./deploykf/argocd-plugin/install_argocd.sh

kubectl get po -n argocd
```

## Install app of apps
```bash
kubectl apply -f deploy/deploykf-app-of-apps.yaml
```


- Set up Kubeflow
- Use Ceph for storage
- Find an application
