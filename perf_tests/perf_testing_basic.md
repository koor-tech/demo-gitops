# Performance Testing in Demo System

For performance testing, we follow the Koor Knowledge Base basically, you can find it [here](https://kb.koor.tech/knowledge/ceph/benchmarking/)

Once you have gone through the guide, you can use the following cheatsheet for demo environment perf testing Here’s a short summary of commands used 

## Disk Performance Commands used with fio

commonly used commands have been adapted to this script.

[https://github.com/koor-tech/demo-gitops/blob/main/perf_tests/test-fio.sh](https://github.com/koor-tech/demo-gitops/blob/main/perf_tests/test-fio.sh) 

## Network Performance using Ancientt:

This step should be performed after you have installed the Kubernetes cluster, we use [ancientt](https://github.com/galexrt/ancientt) tool, which uses iperf3 to perform cross node network testing.

- please refer the [installation guide](https://github.com/galexrt/ancientt#ancientt) to install ancientt on you development enviroment,
- make sure you have right context kubeconfig setup

```console
export KUBECONFIG=~/kubeconfig_staging 
```

- the default [testdefination.example.yaml](https://github.com/galexrt/ancientt/blob/main/testdefinition.example.yaml) can be used for doing our tests

```console
 ancientt git:(main) ✗ cp testdefinition.example.yaml testdefinition.yaml
```

- Run the tests:

```console
ancientt -c testdefination.yaml -y
```
