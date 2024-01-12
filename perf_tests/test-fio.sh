#!/bin/sh


DISK=/dev/sdb

if command -v yum > /dev/null 2>&1; then
    sudo rpm -ihv http://mirrors.kernel.org/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo yum install -y fio git
elif command -v apt-get > /dev/null 2>&1; then 
    sudo apt-get install -y fio git
fi

# source: https://cloud.google.com/compute/docs/disks/benchmarking-pd-performance

# Running this command causes data loss on the second device.
# We strongly recommend using a throwaway VM and disk.
sudo fio --name=write_latency_test \
  --filename=$DISK --filesize=25G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=4 --rw=randwrite --iodepth_batch_submit=4  \
  --iodepth_batch_complete_max=4


sudo fio --name=read_bandwidth_test \
  --filename=$DISK --filesize=25G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=1M --iodepth=64 --rw=read --numjobs=16 --offset_increment=100G \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64


sudo fio --name=read_iops_test \
  --filename=$DISK --filesize=25G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=256 --rw=randread \
  --iodepth_batch_submit=256  --iodepth_batch_complete_max=256


sudo fio --name=read_latency_test \
  --filename=$DISK --filesize=25G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=4K --iodepth=4 --rw=randread \
  --iodepth_batch_submit=4  --iodepth_batch_complete_max=4


sudo fio --name=read_bandwidth_test \
  --filename=$DISK --filesize=25G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --numjobs=4 --thread --offset_increment=500G \
  --bs=1M --iodepth=64 --rw=read \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64


sudo fio --name=write_bandwidth_test \
  --filename=$DISK --filesize=25G \
  --time_based --ramp_time=2s --runtime=1m \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --numjobs=4 --thread --offset_increment=500G \
  --bs=1M --iodepth=64 --rw=write \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64

# Running this command causes data loss on the second device.
# We strongly recommend using a throwaway VM and disk.
sudo fio --name=fill_disk \
  --filename=$DISK --filesize=25G \
  --ioengine=libaio --direct=1 --verify=0 --randrepeat=0 \
  --bs=128K --iodepth=64 --rw=randwrite \
  --iodepth_batch_submit=64  --iodepth_batch_complete_max=64
