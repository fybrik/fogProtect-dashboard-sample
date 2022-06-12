kubectl -n fybrik-system create configmap dashboard-policy --from-file=dashboard-policy.rego
kubectl -n fybrik-system label configmap dashboard-policy openpolicyagent.org/policy=rego
while [[ $(kubectl get cm dashboard-policy -n fybrik-system -o 'jsonpath={.metadata.annotations.openpolicyagent\.org/policy-status}') != '{"status":"ok"}' ]]; do echo "waiting for policy to be applied" && sleep 5; done

