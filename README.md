# FogProtect Usecase
## Build environment
1) Follow the steps of the QuickStart Guide in: https://fybrik.io/v0.4/get-started/quickstart/.  
Displayed here for convenience:  
   1) ```
      kind create cluster --name kind-cluster
   2) ```
      helm repo add jetstack https://charts.jetstack.io 
      helm repo add hashicorp https://helm.releases.hashicorp.com 
      helm repo add fybrik-charts https://fybrik.github.io/charts 
      helm repo update
   3) ```
      helm install cert-manager jetstack/cert-manager \
      --namespace cert-manager \
      --version v1.2.0 \
      --create-namespace \
      --set installCRDs=true \
      --wait --timeout 120s
   4) ```
      git clone https://github.com/fybrik/fybrik.git
      cd fybrik
      helm dependency update charts/vault
      helm install vault charts/vault --create-namespace -n fybrik-system \
      --set "vault.injector.enabled=false" \
      --set "vault.server.dev.enabled=true" \
      --values charts/vault/env/dev/vault-single-cluster-values.yaml
      kubectl wait --for=condition=ready --all pod -n fybrik-system --timeout=120s
   5) ```
      helm install fybrik-crd charts/fybrik-crd -n fybrik-system --wait
      helm install fybrik charts/fybrik --set global.tag=latest -n fybrik-system --wait
   6) Change the current directory to the previous directory:
   ```shell
   cd ..
   ```
2) Create a namespace that will contain the application and the backend data server:  
```shell
kubectl create namespace fogprotect
kubectl config set-context --current --namespace=fogprotect
```
3) Clone this repository, branch `robert-dev`:  
```shell
git clone --branch robert-dev https://github.ibm.com/SALANT/FogProtect.git
```
4) Build the backend data server:  
```shell
cd FogProtect/python/backend
docker build -t querygateway_hack:v1 .
kind load docker-image querygateway_hack:v1 --name kind-cluster
helm install backend-service backend_server-0.1.0.tgz
```
5) Follow the instructions in https://github.com/fybrik/hello-world-read-module#installation 
under the `Installation` section, brought here for convenience:  
   -  After modifying the values in the Makefile as required in the link above, 
      **make sure that the current directory is `FogProtect/`**. Invoke:  
      ```shell
      make docker-build
      make docker-push
      make helm-login
      make helm-verify
      make helm-chart-push
      ```
**Improtant note: make sure that the repositories where the docker image and the helm chart were pushed 
   are public**  
6) Apply the RBAC for the fybrik manager:  
```shell
kubectl apply -f fybrik-system-manager-rbac.yaml -n fybrik-system
```
7) Apply all of the assets, along with the `secret` under the directory `FogProtect/assets` in the 
`forprotect` namespace (the current context of `kubectl`:  
```shell
kubectl apply -f assets/<asset_yaml_file>
```
8) Apply the module in the `fybrik-system` namespace:  
```shell 
kubectl apply -f rest-read-module.yaml -n fybrik-system
```
9) Apply the application in the `fogprotect` namespace (current `kubectl` context):
```shell
kubectl apply -f rest-read-application.yaml
```
10) Wait a couple of seconds after the last step, and then create the port-forwarding:  
```shell
kubectl -n fybrik-blueprints port-forward svc/rest-read 5559:5559
```
11) Start the GUI:
```shell
cd gui/
npm install
npm start
```