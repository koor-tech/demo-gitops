# Demo busybot

This is a simple app to fill the demo environment with dummy data. Here's what it does:

1. List files and read a random set of 5 files.
2. Write a random set of 5 files; allow overwrites.
3. List files and delete a random set of 2 files

Each file is of size 50MB. The files are numbered 00-99.

This will be run using a k8s cronjob every two minutes. The yaml file for the cronjob is included in this folder. CephFS is used since filesystem interface is the easiest to use. We will echo the time it took to write/read each file into logs. To ensure the whole file is read, an md5 will be calculated and out in logs.
