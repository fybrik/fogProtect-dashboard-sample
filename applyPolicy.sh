kubectl -n fybrik-system create configmap rest-read-policy --from-file=dashboard-policy.rego
kubectl -n fybrik-system label configmap rest-read-policy openpolicyagent.org/policy=rego
while [[ $(kubectl get cm rest-read-policy -n fybrik-system -o 'jsonpath={.metadata.annotations.openpolicyagent\.org/policy-status}') != '{"status":"ok"}' ]]; do echo "waiting for policy to be applied" && sleep 5; done
