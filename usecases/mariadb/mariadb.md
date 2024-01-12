# Installing database instance (mariadb) with Koor Storage Distribution

We’ll use rook-ceph-block storage class for backing the mariadb database.
suggestion: we change the block size to use 16kB object size while deploying block storage class.

```code
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata:
  name: replicapool
  namespace: koor-ceph # namespace:cluster
spec:
  failureDomain: host
  replicated:
    size: 3
    # Disallow setting pool with replica 1, this could lead to data loss without recovery.
    # Make sure you're *ABSOLUTELY CERTAIN* that is what you want
    requireSafeReplicaSize: true
    # gives a hint (%) to Ceph in terms of expected consumption of the total cluster capacity of a given pool
    # for more info: https://docs.ceph.com/docs/master/rados/operations/placement-groups/#specifying-expected-pool-size
    #targetSizeRatio: .5
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-ceph-block
# Change "rook-ceph" provisioner prefix to match the operator namespace if needed
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  # clusterID is the namespace where the rook cluster is running
  # If you change this namespace, also change the namespace below where the secret namespaces are defined
  clusterID: koor-ceph # namespace:cluster

  # If you want to use erasure coded pool with RBD, you need to create
  # two pools. one erasure coded and one replicated.
  # You need to specify the replicated pool here in the `pool` parameter, it is
  # used for the metadata of the images.
  # The erasure coded pool must be set as the `dataPool` parameter below.
  #dataPool: ec-data-pool
  pool: replicapool

  # (optional) mapOptions is a comma-separated list of map options.
  # For krbd options refer
  # https://docs.ceph.com/docs/master/man/8/rbd/#kernel-rbd-krbd-options
  # For nbd options refer
  # https://docs.ceph.com/docs/master/man/8/rbd-nbd/#options
  # mapOptions: lock_on_read,queue_depth=1024

  # (optional) unmapOptions is a comma-separated list of unmap options.
  # For krbd options refer
  # https://docs.ceph.com/docs/master/man/8/rbd/#kernel-rbd-krbd-options
  # For nbd options refer
  # https://docs.ceph.com/docs/master/man/8/rbd-nbd/#options
  # unmapOptions: force

   # (optional) Set it to true to encrypt each volume with encryption keys
   # from a key management system (KMS)
   # encrypted: "true"

   # (optional) Use external key management system (KMS) for encryption key by
   # specifying a unique ID matching a KMS ConfigMap. The ID is only used for
   # correlation to configmap entry.
   # encryptionKMSID: <kms-config-id>

  # RBD image format. Defaults to "2".
  imageFormat: "2"

  # RBD image features
  # Available for imageFormat: "2". Older releases of CSI RBD
  # support only the `layering` feature. The Linux kernel (KRBD) supports the
  # full complement of features as of 5.4
  # `layering` alone corresponds to Ceph's bitfield value of "2" ;
  # `layering` + `fast-diff` + `object-map` + `deep-flatten` + `exclusive-lock` together
  # correspond to Ceph's OR'd bitfield value of "63". Here we use
  # a symbolic, comma-separated format:
  # For 5.4 or later kernels:
  #imageFeatures: layering,fast-diff,object-map,deep-flatten,exclusive-lock
  # For 5.3 or earlier kernels:
  imageFeatures: layering
  objectSize: 16K

  # The secrets contain Ceph admin credentials. These are generated automatically by the operator
  # in the same namespace as the cluster.
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: koor-ceph # namespace:cluster
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: koor-ceph # namespace:cluster
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: koor-ceph # namespace:cluster
  # Specify the filesystem type of the volume. If not specified, csi-provisioner
  # will set default as `ext4`. Note that `xfs` is not recommended due to potential deadlock
  # in hyperconverged settings where the volume is mounted on the same node as the osds.
  csi.storage.k8s.io/fstype: ext4
# uncomment the following to use rbd-nbd as mounter on supported nodes
# **IMPORTANT**: CephCSI v3.4.0 onwards a volume healer functionality is added to reattach
# the PVC to application pod if nodeplugin pod restart.
# Its still in Alpha support. Therefore, this option is not recommended for production use.
#mounter: rbd-nbd
allowVolumeExpansion: true
reclaimPolicy: Delete

```
we can see that now in the mariadb rbd image volume with 16kb object size

```code
kubectl -n koor-ceph exec -it deploy/rook-ceph-tools -- rbd info ceph-blockpool/csi-vol-cab262d6-cc0c-4981-a341-d23c17b1e119 
rbd image 'csi-vol-cab262d6-cc0c-4981-a341-d23c17b1e119':
	size 8 GiB in 524288 objects
	order 14 (16 KiB objects)
	snapshot_count: 0
	id: 17db1059fb32c1
	block_name_prefix: rbd_data.17db1059fb32c1
	format: 2
	features: layering
	op_features:
	flags:
	create_timestamp: Wed Aug 16 12:38:23 2023
	access_timestamp: Wed Aug 16 12:38:23 2023
	modify_timestamp: Wed Aug 16 12:38:23 2023
```

this will help improve the write performance on average.
We are using helm charts for installing mariadb, with the mariadb values altered to use rook-ceph-block storage class, eg:
find the updated values.yaml for mariadb [here](https://github.com/helm/charts/blob/master/stable/mariadb/values.yaml)

```code
## Global Docker image parameters
## Please, note that this will override the image parameters, including dependencies, configured to use the global value
## Current available global Docker image parameters: imageRegistry and imagePullSecrets
##
# global:
#   imageRegistry: myRegistryName
#   imagePullSecrets:
#     - myRegistryKeySecretName
#   storageClass: myStorageClass

## Use an alternate scheduler, e.g. "stork".
## ref: https://kubernetes.io/docs/tasks/administer-cluster/configure-multiple-schedulers/
##
# schedulerName:

## Bitnami MariaDB image
## ref: https://hub.docker.com/r/bitnami/mariadb/tags/
##
image:
  registry: docker.io
  repository: bitnami/mariadb
  tag: 10.3.22-debian-10-r27
  ## Specify a imagePullPolicy
  ## Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
  ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
  ##
  pullPolicy: IfNotPresent
  ## Optionally specify an array of imagePullSecrets.
  ## Secrets must be manually created in the namespace.
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistryKeySecretName

  ## Set to true if you would like to see extra information on logs
  ## It turns BASH and NAMI debugging in minideb
  ## ref:  https://github.com/bitnami/minideb-extras/#turn-on-bash-debugging
  debug: false

## String to partially override mariadb.fullname template (will maintain the release name)
##
# nameOverride:

## String to fully override mariadb.fullname template
##
# fullnameOverride:

## Init containers parameters:
## volumePermissions: Change the owner and group of the persistent volume mountpoint to runAsUser:fsGroup values from the securityContext section.
##
volumePermissions:
  enabled: false
  image:
    registry: docker.io
    repository: bitnami/minideb
    tag: buster
    pullPolicy: Always
    ## Optionally specify an array of imagePullSecrets.
    ## Secrets must be manually created in the namespace.
    ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
    ##
    # pullSecrets:
    #   - myRegistryKeySecretName
  resources: {}

service:
  ## Kubernetes service type, ClusterIP and NodePort are supported at present
  type: ClusterIP
  # clusterIp:
  #   master: xx.xx.xx.xx
  #   slave: xx.xx.xx.xx
  port: 3306
  ## Specify the nodePort value for the LoadBalancer and NodePort service types.
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
  ##
  # nodePort:
  #   master: 30001
  #   slave: 30002

## Pods Service Account
## ref: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/
serviceAccount:
  ## Specifies whether a ServiceAccount should be created
  ##
  create: false
  ## The name of the ServiceAccount to use.
  ## If not set and create is true, a name is generated using the mariadb.fullname template
  # name:

## Role Based Access
## Ref: https://kubernetes.io/docs/admin/authorization/rbac/
##
rbac:
  create: false

## Pod Security Context
## ref: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
##
securityContext:
  enabled: true
  fsGroup: 1001
  runAsUser: 1001

## Use existing secret (ignores root, db and replication passwords)
##
# existingSecret:

## MariaDB admin credentials
##
rootUser:
  ## MariaDB admin password
  ## ref: https://github.com/bitnami/bitnami-docker-mariadb#setting-the-root-password-on-first-run
  ##
  password: ""
  ## Option to force users to specify a password. That is required for 'helm upgrade' to work properly.
  ## If it is not force, a random password will be generated.
  ##
  forcePassword: false
  ## Mount admin password as a file instead of using an environment variable
  ##
  injectSecretsAsVolume: false

## Custom user/db credentials
##
db:
  ## MariaDB username and password
  ## ref: https://github.com/bitnami/bitnami-docker-mariadb#creating-a-database-user-on-first-run
  ##
  user: ""
  password: ""
  ## Database to create
  ## ref: https://github.com/bitnami/bitnami-docker-mariadb#creating-a-database-on-first-run
  ##
  name: my_database
  ## Option to force users to specify a password. That is required for 'helm upgrade' to work properly.
  ## If it is not force, a random password will be generated.
  ##
  forcePassword: false
  ## Mount user password as a file instead of using an environment variable
  ##
  injectSecretsAsVolume: false

## Replication configuration
##
replication:
  ## Enable replication. This enables the creation of replicas of MariaDB. If false, only a
  ## master deployment would be created
  ##
  enabled: true
  ## MariaDB replication user
  ## ref: https://github.com/bitnami/bitnami-docker-mariadb#setting-up-a-replication-cluster
  ##
  user: replicator
  ## MariaDB replication user password
  ## ref: https://github.com/bitnami/bitnami-docker-mariadb#setting-up-a-replication-cluster
  ##
  password: ""
  ## Option to force users to specify a password. That is required for 'helm upgrade' to work properly.
  ## If it is not force, a random password will be generated.
  ##
  forcePassword: false
  ## Mount replication user password as a file instead of using an environment variable
  ##
  injectSecretsAsVolume: false

## initdb scripts
## Specify dictionary of scripts to be run at first boot
## Alternatively, you can put your scripts under the files/docker-entrypoint-initdb.d directory
##
# initdbScripts:
#   my_init_script.sh: |
#      #!/bin/sh
#      echo "Do something."
#
## ConfigMap with scripts to be run at first boot
## Note: This will override initdbScripts
# initdbScriptsConfigMap:

master:
  ## Mariadb Master additional pod annotations
  ## ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
  # annotations:
  #   key: value
  #   another-key: another-value

  ## MariaDB additional command line flags
  ## Can be used to specify command line flags, for example:
  ##
  ## extraFlags: "--max-connect-errors=1000 --max_connections=155"

  ## Affinity for pod assignment
  ## Ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ##
  affinity: {}

  ## Kept for backwards compatibility. You can now disable it by removing it.
  ## if you wish to set it through master.affinity.podAntiAffinity instead.
  ##
  antiAffinity: soft

  ## Node labels for pod assignment
  ## Ref: https://kubernetes.io/docs/user-guide/node-selection/
  ##
  nodeSelector: {}

  ## Tolerations for pod assignment
  ## Ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
  ##
  tolerations: []

  ## updateStrategy for MariaDB Master StatefulSet
  ## ref: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies
  updateStrategy:
    type: RollingUpdate

  ## Enable persistence using Persistent Volume Claims
  ## ref: http://kubernetes.io/docs/user-guide/persistent-volumes/
  ##
  persistence:
    ## If true, use a Persistent Volume Claim, If false, use emptyDir
    ##
    enabled: true
    # Enable persistence using an existing PVC
    # existingClaim:
    # Subdirectory of the volume to mount
    # subPath:
    mountPath: /bitnami/mariadb
    ## Persistent Volume Storage Class
    ## If defined, storageClassName: <storageClass>
    ## If set to "-", storageClassName: "", which disables dynamic provisioning
    ## If undefined (the default) or set to null, no storageClassName spec is
    ##   set, choosing the default provisioner.  (gp2 on AWS, standard on
    ##   GKE, AWS & OpenStack)
    ##
    storageClass: "rook-ceph-block"
    ## Persistent Volume Claim annotations
    ##
    annotations: {}
    ## Persistent Volume Access Mode
    ##
    accessModes:
    - ReadWriteOnce
    ## Persistent Volume size
    ##
    size: 8Gi

  extraInitContainers: |
  # - name: do-something
  #   image: busybox
  #   command: ['do', 'something']

  ## An array to add extra environment variables
  ## For example:
  ## extraEnvVars:
  ##  - name: TZ
  ##    value: "Europe/Paris"
  ##
  # extraEnvVars:

  ## Configure MySQL with a custom my.cnf file
  ## ref: https://mysql.com/kb/en/mysql/configuring-mysql-with-mycnf/#example-of-configuration-file
  ##
  config: |-
    [mysqld]
    skip-name-resolve
    explicit_defaults_for_timestamp
    basedir=/opt/bitnami/mariadb
    plugin_dir=/opt/bitnami/mariadb/plugin
    port=3306
    socket=/opt/bitnami/mariadb/tmp/mysql.sock
    tmpdir=/opt/bitnami/mariadb/tmp
    max_allowed_packet=16M
    bind-address=0.0.0.0
    pid-file=/opt/bitnami/mariadb/tmp/mysqld.pid
    log-error=/opt/bitnami/mariadb/logs/mysqld.log
    character-set-server=UTF8
    collation-server=utf8_general_ci

    [client]
    port=3306
    socket=/opt/bitnami/mariadb/tmp/mysql.sock
    default-character-set=UTF8
    plugin_dir=/opt/bitnami/mariadb/plugin

    [manager]
    port=3306
    socket=/opt/bitnami/mariadb/tmp/mysql.sock
    pid-file=/opt/bitnami/mariadb/tmp/mysqld.pid

  ## Configure master resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  resources: {}
  livenessProbe:
    enabled: true
    ##
    ## Initializing the database could take some time
    initialDelaySeconds: 120
    ##
    ## Default Kubernetes values
    periodSeconds: 10
    timeoutSeconds: 1
    successThreshold: 1
    failureThreshold: 3
  readinessProbe:
    enabled: true
    initialDelaySeconds: 30
    ##
    ## Default Kubernetes values
    periodSeconds: 10
    timeoutSeconds: 1
    successThreshold: 1
    failureThreshold: 3

  podDisruptionBudget:
    enabled: false
    minAvailable: 1
    # maxUnavailable: 1

  ## Allow customization of the service resource
  ##
  service:
    ## Add custom annotations to the service
    ##
    annotations: {}
      # external-dns.alpha.kubernetes.io/hostname: db.example.com

slave:
  replicas: 1

  ## Mariadb Slave additional pod annotations
  ## ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
  # annotations:
  #   key: value
  #   another-key: another-value

  ## MariaDB additional command line flags
  ## Can be used to specify command line flags, for example:
  ##
  ## extraFlags: "--max-connect-errors=1000 --max_connections=155"

  ## Affinity for pod assignment
  ## Ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ##
  affinity: {}

  ## Kept for backwards compatibility. You can now disable it by removing it.
  ## if you wish to set it through slave.affinity.podAntiAffinity instead.
  ##
  antiAffinity: soft

  ## Node labels for pod assignment
  ## Ref: https://kubernetes.io/docs/user-guide/node-selection/
  ##
  nodeSelector: {}

  ## Tolerations for pod assignment
  ## Ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
  ##
  tolerations: []

  ## updateStrategy for MariaDB Slave StatefulSet
  ## ref: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies
  updateStrategy:
    type: RollingUpdate

  persistence:
    ## If true, use a Persistent Volume Claim, If false, use emptyDir
    ##
    enabled: true
    # storageClass: "-"
    annotations:
    accessModes:
    - ReadWriteOnce
    ## Persistent Volume size
    ##
    size: 8Gi

  extraInitContainers: |
  # - name: do-something
  #   image: busybox
  #   command: ['do', 'something']

  ## An array to add extra environment variables
  ## For example:
  ## extraEnvVars:
  ##  - name: TZ
  ##    value: "Europe/Paris"
  ##
  # extraEnvVars:

  ## Configure MySQL slave with a custom my.cnf file
  ## ref: https://mysql.com/kb/en/mysql/configuring-mysql-with-mycnf/#example-of-configuration-file
  ##
  config: |-
    [mysqld]
    skip-name-resolve
    explicit_defaults_for_timestamp
    basedir=/opt/bitnami/mariadb
    port=3306
    socket=/opt/bitnami/mariadb/tmp/mysql.sock
    tmpdir=/opt/bitnami/mariadb/tmp
    max_allowed_packet=16M
    bind-address=0.0.0.0
    pid-file=/opt/bitnami/mariadb/tmp/mysqld.pid
    log-error=/opt/bitnami/mariadb/logs/mysqld.log
    character-set-server=UTF8
    collation-server=utf8_general_ci

    [client]
    port=3306
    socket=/opt/bitnami/mariadb/tmp/mysql.sock
    default-character-set=UTF8

    [manager]
    port=3306
    socket=/opt/bitnami/mariadb/tmp/mysql.sock
    pid-file=/opt/bitnami/mariadb/tmp/mysqld.pid

  ##
  ## Configure slave resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  resources: {}
  livenessProbe:
    enabled: true
    ##
    ## Initializing the database could take some time
    initialDelaySeconds: 120
    ##
    ## Default Kubernetes values
    periodSeconds: 10
    timeoutSeconds: 1
    successThreshold: 1
    failureThreshold: 3
  readinessProbe:
    enabled: true
    initialDelaySeconds: 45
    ##
    ## Default Kubernetes values
    periodSeconds: 10
    timeoutSeconds: 1
    successThreshold: 1
    failureThreshold: 3

  podDisruptionBudget:
    enabled: false
    minAvailable: 1
    # maxUnavailable: 1

  ## Allow customization of the service resource
  ##
  service:
    ## Add custom annotations to the service
    ##
    annotations: {}
      # external-dns.alpha.kubernetes.io/hostname: rodb.example.com

metrics:
  enabled: false
  image:
    registry: docker.io
    repository: bitnami/mysqld-exporter
    tag: 0.12.1-debian-10-r27
    pullPolicy: IfNotPresent
    ## Optionally specify an array of imagePullSecrets.
    ## Secrets must be manually created in the namespace.
    ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
    ##
    # pullSecrets:
    #   - myRegistryKeySecretName
  resources: {}
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9104"

  ## Extra args to be passed to mysqld_exporter
  ## ref: https://github.com/prometheus/mysqld_exporter/
  ##
  extraArgs:
    master: []
    slave: []
      # - --collect.auto_increment.columns
      # - --collect.binlog_size
      # - --collect.engine_innodb_status
      # - --collect.engine_tokudb_status
      # - --collect.global_status
      # - --collect.global_variables
      # - --collect.info_schema.clientstats
      # - --collect.info_schema.innodb_metrics
      # - --collect.info_schema.innodb_tablespaces
      # - --collect.info_schema.innodb_cmp
      # - --collect.info_schema.innodb_cmpmem
      # - --collect.info_schema.processlist
      # - --collect.info_schema.processlist.min_time
      # - --collect.info_schema.query_response_time
      # - --collect.info_schema.tables
      # - --collect.info_schema.tables.databases
      # - --collect.info_schema.tablestats
      # - --collect.info_schema.userstats
      # - --collect.perf_schema.eventsstatements
      # - --collect.perf_schema.eventsstatements.digest_text_limit
      # - --collect.perf_schema.eventsstatements.limit
      # - --collect.perf_schema.eventsstatements.timelimit
      # - --collect.perf_schema.eventswaits
      # - --collect.perf_schema.file_events
      # - --collect.perf_schema.file_instances
      # - --collect.perf_schema.indexiowaits
      # - --collect.perf_schema.tableiowaits
      # - --collect.perf_schema.tablelocks
      # - --collect.perf_schema.replication_group_member_stats
      # - --collect.slave_status
      # - --collect.slave_hosts
      # - --collect.heartbeat
      # - --collect.heartbeat.database
      # - --collect.heartbeat.table

  livenessProbe:
    enabled: true
    ##
    ## Initializing the database could take some time
    initialDelaySeconds: 120
    ##
    ## Default Kubernetes values
    periodSeconds: 10
    timeoutSeconds: 1
    successThreshold: 1
    failureThreshold: 3
  readinessProbe:
    enabled: true
    initialDelaySeconds: 30
    ##
    ## Default Kubernetes values
    periodSeconds: 10
    timeoutSeconds: 1
    successThreshold: 1
    failureThreshold: 3

  # Enable this if you're using https://github.com/coreos/prometheus-operator
  serviceMonitor:
    enabled: false
    ## Specify a namespace if needed
    # namespace: monitoring
    # fallback to the prometheus default unless specified
    # interval: 10s
    # scrapeTimeout: 10s
    ## Defaults to what's used if you follow CoreOS [Prometheus Install Instructions](https://github.com/helm/charts/tree/master/stable/prometheus-operator#tldr)
    ## [Prometheus Selector Label](https://github.com/helm/charts/tree/master/stable/prometheus-operator#prometheus-operator-1)
    ## [Kube Prometheus Selector Label](https://github.com/helm/charts/tree/master/stable/prometheus-operator#exporters)
    selector:
      prometheus: kube-prometheus

## Bats Framework (= Bash Automated Testing System) is needed to test if MariaDB is accessible
## See test-runner.yaml and tests.yaml for details.
## To run the tests after the deployment, enter "helm test <release-name>".
tests:
  enabled: true
  # resources: {}
  testFramework:
    image:
      registry: docker.io
      repository: dduportal/bats
      tag: 0.4.0
    # resources: {}
```

take into consideration 8GB and 24GB will be used by mariadb

```code 
 helm install my-release oci://registry-1.docker.io/bitnamicharts/mariadb -f mariadb_values.yaml
```

2. after deploying we can connect to the client:

```
 ** Please be patient while the chart is being deployed **

Tip:

  Watch the deployment status using the command: kubectl get pods -w --namespace mariadb -l app.kubernetes.io/instance=mariadb

Services:

  echo Primary: mariadb.mariadb.svc.cluster.local:3306

Administrator credentials:

  Username: root
  Password : $(kubectl get secret --namespace mariadb mariadb -o jsonpath="{.data.mariadb-root-password}" | base64 -d)

To connect to your database:

  1. Run a pod that you can use as a client:

      kubectl run mariadb-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mariadb:10.3.22-debian-10-r27 --namespace mariadb --command -- bash

  2. To connect to primary service (read/write):

 ROOT_PASSWORD=$(kubectl get secret --namespace mariadb mariadb -o  jsonpath="{.data.mariadb-root-password}" | base64 -d)
    mysql -h mariadb.mariadb.svc.cluster.local -uroot -p $ROOT_PASSWORD  my_database
```
To upgrade this helm chart:

  1. Obtain the password as described on the 'Administrator credentials' section and set the 'auth.rootPassword' parameter as shown below:

```code
      ROOT_PASSWORD=$(kubectl get secret --namespace mariadb mariadb -o jsonpath="{.data.mariadb-root-password}" | base64 -d)
      helm upgrade --namespace mariadb mariadb oci://registry-1.docker.io/bitnamicharts/mariadb --set auth.rootPassword=$ROOT_PASSWORD
```

We used mock data for inserting test data to my_database and then inserted mock data using [this mock data generator](https://www.mockaroo.com/) 
to run the mysql script/query in the mariadb client directly you can use

```code
kubectl exec -it mariadb-client --namespace mariadb -- mysql -h mariadb.mariadb.svc.cluster.local -uroot -p $ROOT_PASSWORD my_database < mock_data.sql
```
You can monitor the IOPS and other metrics during data insertion and other queries using ceph dashboard it might look something like the below:




