# Demo busybot

This is a simple app to fill the demo environment with dummy data. Here's what it does:

1. Read a random set of 5 files.
2. Write a random set of 5 files; allow overwrites.

Each file is of size 50MB. The files are numbered 00-99. All files will be generated beforehand to prevent a case where a file is missing.

This will be run using a k8s cronjob every two minutes. The yaml file for the cronjob is included in this folder. CephFS is used since filesystem interface is the easiest to use. We will echo the time it took to write/read each file into logs. To ensure the whole file is read, an md5 will be calculated and out in logs.
