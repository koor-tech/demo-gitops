^[write_latency_test: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=4
fio-3.28
Starting 1 process
Jobs: 1 (f=1): [w(1)][100.0%][w=4008KiB/s][w=1002 IOPS][eta 00m:00s]
write_latency_test: (groupid=0, jobs=1): err= 0: pid=1804641: Fri Oct 20 12:51:21 2023
  write: IOPS=941, BW=3765KiB/s (3855kB/s)(221MiB/60008msec); 0 zone resets
    slat (usec): min=2, max=1018, avg=19.85, stdev=13.91
    clat (msec): min=2, max=143, avg= 4.23, stdev= 3.01
     lat (msec): min=2, max=143, avg= 4.25, stdev= 3.01
    clat percentiles (usec):
     |  1.00th=[ 2343],  5.00th=[ 2474], 10.00th=[ 2573], 20.00th=[ 2671],
     | 30.00th=[ 2769], 40.00th=[ 2900], 50.00th=[ 3064], 60.00th=[ 3359],
     | 70.00th=[ 3949], 80.00th=[ 5342], 90.00th=[ 7439], 95.00th=[ 9372],
     | 99.00th=[15533], 99.50th=[19268], 99.90th=[31327], 99.95th=[37487],
     | 99.99th=[56886]
   bw (  KiB/s): min= 1891, max= 4665, per=100.00%, avg=3768.13, stdev=650.48, samples=120
   iops        : min=  472, max= 1166, avg=941.87, stdev=162.66, samples=120
  lat (msec)   : 4=70.65%, 10=25.29%, 20=3.64%, 50=0.42%, 100=0.01%
  lat (msec)   : 250=0.01%
  cpu          : usr=0.83%, sys=2.88%, ctx=53031, majf=0, minf=58
  IO depths    : 1=0.1%, 2=4.3%, 4=95.7%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwts: total=0,56475,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=4

Run status group 0 (all jobs):
  WRITE: bw=3765KiB/s (3855kB/s), 3765KiB/s-3765KiB/s (3855kB/s-3855kB/s), io=221MiB (231MB), run=60008-60008msec

Disk stats (read/write):
  sdb: ios=51/57280, merge=0/0, ticks=66/246399, in_queue=246465, util=100.00%
read_bandwidth_test: (g=0): rw=read, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, (T) 1024KiB-1024KiB, ioengine=libaio, iodepth=64
...
fio-3.28
Starting 16 processes
Jobs: 1 (f=1): [R(1),_(15)][100.0%][r=12.4GiB/s][r=12.7k IOPS][eta 00m:00s]
read_bandwidth_test: (groupid=0, jobs=1): err= 0: pid=1805509: Fri Oct 20 12:52:23 2023
  read: IOPS=11.8k, BW=11.6GiB/s (12.4GB/s)(693GiB/60005msec)
    slat (usec): min=14, max=7328, avg=660.86, stdev=703.42
    clat (nsec): min=1753, max=47212k, avg=4687412.50, stdev=1895038.79
     lat (usec): min=696, max=48547, avg=5348.26, stdev=1711.34
    clat percentiles (usec):
     |  1.00th=[   50],  5.00th=[ 1680], 10.00th=[ 2245], 20.00th=[ 3032],
     | 30.00th=[ 3654], 40.00th=[ 4228], 50.00th=[ 4686], 60.00th=[ 5211],
     | 70.00th=[ 5669], 80.00th=[ 6259], 90.00th=[ 7046], 95.00th=[ 7701],
     | 99.00th=[ 9110], 99.50th=[ 9765], 99.90th=[11600], 99.95th=[13304],
     | 99.99th=[21627]
   bw (  MiB/s): min= 9835, max=12974, per=100.00%, avg=11840.75, stdev=643.64, samples=120
   iops        : min= 9835, max=12974, avg=11840.48, stdev=643.66, samples=120
  lat (usec)   : 2=0.01%, 4=0.06%, 10=0.24%, 20=0.43%, 50=0.28%
  lat (usec)   : 100=0.06%, 250=0.07%, 500=0.16%, 750=0.24%, 1000=0.42%
  lat (msec)   : 2=5.61%, 4=28.52%, 10=63.53%, 20=0.37%, 50=0.01%
  cpu          : usr=2.54%, sys=60.03%, ctx=73807, majf=0, minf=58
  IO depths    : 1=0.0%, 2=0.0%, 4=0.0%, 8=0.1%, 16=1.6%, 32=79.7%, >=64=18.6%
     submit    : 0=0.0%, 4=68.9%, 8=12.4%, 16=12.3%, 32=5.5%, 64=0.9%, >=64=0.0%
     complete  : 0=0.0%, 4=68.9%, 8=11.3%, 16=12.1%, 32=6.2%, 64=1.5%, >=64=0.0%
     issued rwts: total=709694,0,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=64

Run status group 0 (all jobs):
   READ: bw=11.6GiB/s (12.4GB/s), 11.6GiB/s-11.6GiB/s (12.4GB/s-12.4GB/s), io=693GiB (744GB), run=60005-60005msec

Disk stats (read/write):
  sdb: ios=828854/0, merge=137189/0, ticks=3815192/0, in_queue=3815192, util=99.95%
read_iops_test: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=256
fio-3.28
Starting 1 process
Jobs: 1 (f=1): [r(1)][100.0%][r=292MiB/s][r=74.7k IOPS][eta 00m:00s]
read_iops_test: (groupid=0, jobs=1): err= 0: pid=1806351: Fri Oct 20 12:53:25 2023
  read: IOPS=82.8k, BW=324MiB/s (339MB/s)(19.0GiB/60005msec)
    slat (nsec): min=1683, max=3222.8k, avg=87309.58, stdev=185527.66
    clat (usec): min=4, max=237101, avg=2979.93, stdev=1288.98
     lat (usec): min=367, max=237192, avg=3067.24, stdev=1269.02
    clat percentiles (usec):
     |  1.00th=[  963],  5.00th=[ 1516], 10.00th=[ 1860], 20.00th=[ 2180],
     | 30.00th=[ 2376], 40.00th=[ 2540], 50.00th=[ 2769], 60.00th=[ 2999],
     | 70.00th=[ 3261], 80.00th=[ 3654], 90.00th=[ 4359], 95.00th=[ 5080],
     | 99.00th=[ 7177], 99.50th=[ 8225], 99.90th=[10683], 99.95th=[12125],
     | 99.99th=[17957]
   bw (  KiB/s): min=229771, max=399608, per=100.00%, avg=331689.24, stdev=36676.62, samples=120
   iops        : min=57442, max=99902, avg=82922.17, stdev=9169.21, samples=120
  lat (usec)   : 10=0.02%, 20=0.03%, 50=0.01%, 100=0.01%, 250=0.01%
  lat (usec)   : 500=0.03%, 750=0.26%, 1000=0.78%
  lat (msec)   : 2=12.33%, 4=72.64%, 10=13.75%, 20=0.14%, 50=0.01%
  lat (msec)   : 100=0.01%, 250=0.01%
  cpu          : usr=7.31%, sys=25.38%, ctx=982992, majf=0, minf=58
  IO depths    : 1=0.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.1%, >=64=100.0%
     submit    : 0=0.0%, 4=59.5%, 8=19.3%, 16=13.6%, 32=5.9%, 64=1.4%, >=64=0.3%
     complete  : 0=0.0%, 4=59.2%, 8=19.3%, 16=13.7%, 32=6.0%, 64=1.4%, >=64=0.3%
     issued rwts: total=4970229,0,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=256

Run status group 0 (all jobs):
   READ: bw=324MiB/s (339MB/s), 324MiB/s-324MiB/s (339MB/s-339MB/s), io=19.0GiB (20.4GB), run=60005-60005msec

Disk stats (read/write):
  sdb: ios=5127121/0, merge=43/0, ticks=15113345/0, in_queue=15113345, util=99.95%
read_latency_test: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=4
fio-3.28
Starting 1 process
Jobs: 1 (f=1): [r(1)][100.0%][r=24.9MiB/s][r=6365 IOPS][eta 00m:00s]
read_latency_test: (groupid=0, jobs=1): err= 0: pid=1807269: Fri Oct 20 12:54:28 2023
  read: IOPS=6237, BW=24.4MiB/s (25.5MB/s)(1462MiB/60001msec)
    slat (nsec): min=1913, max=2153.8k, avg=13782.54, stdev=13784.29
    clat (usec): min=4, max=49631, avg=623.81, stdev=354.88
     lat (usec): min=294, max=49643, avg=637.66, stdev=355.56
    clat percentiles (usec):
     |  1.00th=[  420],  5.00th=[  461], 10.00th=[  486], 20.00th=[  519],
     | 30.00th=[  537], 40.00th=[  562], 50.00th=[  578], 60.00th=[  603],
     | 70.00th=[  627], 80.00th=[  660], 90.00th=[  725], 95.00th=[  832],
     | 99.00th=[ 1500], 99.50th=[ 2573], 99.90th=[ 5145], 99.95th=[ 6194],
     | 99.99th=[10290]
   bw (  KiB/s): min=22068, max=27848, per=100.00%, avg=24973.04, stdev=1050.40, samples=120
   iops        : min= 5517, max= 6962, avg=6243.12, stdev=262.58, samples=120
  lat (usec)   : 10=0.01%, 20=0.01%, 100=0.01%, 250=0.01%, 500=13.66%
  lat (usec)   : 750=78.16%, 1000=5.64%
  lat (msec)   : 2=1.86%, 4=0.47%, 10=0.21%, 20=0.01%, 50=0.01%
  cpu          : usr=3.23%, sys=10.05%, ctx=273971, majf=0, minf=58
  IO depths    : 1=0.5%, 2=17.9%, 4=81.5%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwts: total=374268,0,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=4

Run status group 0 (all jobs):
   READ: bw=24.4MiB/s (25.5MB/s), 24.4MiB/s-24.4MiB/s (25.5MB/s-25.5MB/s), io=1462MiB (1533MB), run=60001-60001msec

Disk stats (read/write):
  sdb: ios=386679/0, merge=0/0, ticks=240437/0, in_queue=240437, util=99.93%
read_bandwidth_test: (g=0): rw=read, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, (T) 1024KiB-1024KiB, ioengine=libaio, iodepth=64
...
fio-3.28
Starting 4 threads
read_bandwidth_test: you need to specify valid offset=
read_bandwidth_test: you need to specify valid offset=
read_bandwidth_test: you need to specify valid offset=
Jobs: 1 (f=1): [R(1),_(3)][100.0%][r=12.4GiB/s][r=12.7k IOPS][eta 00m:00s]
read_bandwidth_test: (groupid=0, jobs=1): err= 0: pid=1808117: Fri Oct 20 12:55:30 2023
  read: IOPS=11.8k, BW=11.6GiB/s (12.4GB/s)(694GiB/60004msec)
    slat (usec): min=14, max=8446, avg=653.75, stdev=687.84
    clat (nsec): min=1874, max=95941k, avg=4692154.30, stdev=1870182.70
     lat (usec): min=594, max=96107, avg=5345.89, stdev=1704.41
    clat percentiles (usec):
     |  1.00th=[  215],  5.00th=[ 1745], 10.00th=[ 2311], 20.00th=[ 3097],
     | 30.00th=[ 3687], 40.00th=[ 4228], 50.00th=[ 4686], 60.00th=[ 5145],
     | 70.00th=[ 5669], 80.00th=[ 6194], 90.00th=[ 6980], 95.00th=[ 7635],
     | 99.00th=[ 9110], 99.50th=[ 9765], 99.90th=[11863], 99.95th=[13435],
     | 99.99th=[25035]
   bw (  MiB/s): min=10064, max=12881, per=100.00%, avg=11852.54, stdev=673.97, samples=120
   iops        : min=10064, max=12881, avg=11852.30, stdev=673.96, samples=120
  lat (usec)   : 2=0.01%, 4=0.06%, 10=0.23%, 20=0.45%, 50=0.18%
  lat (usec)   : 100=0.04%, 250=0.06%, 500=0.13%, 750=0.22%, 1000=0.38%
  lat (msec)   : 2=5.20%, 4=28.51%, 10=64.16%, 20=0.37%, 50=0.02%
  lat (msec)   : 100=0.01%
  cpu          : usr=2.28%, sys=60.62%, ctx=68939, majf=0, minf=0
  IO depths    : 1=0.1%, 2=0.0%, 4=0.1%, 8=0.1%, 16=1.6%, 32=80.1%, >=64=18.2%
     submit    : 0=0.0%, 4=66.2%, 8=14.0%, 16=13.4%, 32=5.5%, 64=0.8%, >=64=0.0%
     complete  : 0=0.0%, 4=65.9%, 8=12.9%, 16=13.5%, 32=6.3%, 64=1.5%, >=64=0.0%
     issued rwts: total=710424,0,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=64

Run status group 0 (all jobs):
   READ: bw=11.6GiB/s (12.4GB/s), 11.6GiB/s-11.6GiB/s (12.4GB/s-12.4GB/s), io=694GiB (745GB), run=60004-60004msec

Disk stats (read/write):
  sdb: ios=844587/0, merge=158255/0, ticks=3867150/0, in_queue=3867150, util=99.95%
write_bandwidth_test: (g=0): rw=write, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, (T) 1024KiB-1024KiB, ioengine=libaio, iodepth=64
...
fio-3.28
Starting 4 threads
write_bandwidth_test: you need to specify valid offset=
write_bandwidth_test: you need to specify valid offset=
write_bandwidth_test: you need to specify valid offset=
Jobs: 1 (f=1): [W(1),_(3)][100.0%][w=1332MiB/s][w=1332 IOPS][eta 00m:00s]
write_bandwidth_test: (groupid=0, jobs=1): err= 0: pid=1808967: Fri Oct 20 12:56:32 2023
  write: IOPS=1299, BW=1300MiB/s (1364MB/s)(76.3GiB/60065msec); 0 zone resets
    slat (usec): min=30, max=5479, avg=283.21, stdev=233.35
    clat (msec): min=8, max=378, avg=48.86, stdev=20.00
     lat (msec): min=8, max=378, avg=49.14, stdev=20.02
    clat percentiles (msec):
     |  1.00th=[   12],  5.00th=[   15], 10.00th=[   20], 20.00th=[   41],
     | 30.00th=[   43], 40.00th=[   46], 50.00th=[   48], 60.00th=[   51],
     | 70.00th=[   54], 80.00th=[   59], 90.00th=[   70], 95.00th=[   83],
     | 99.00th=[  112], 99.50th=[  127], 99.90th=[  180], 99.95th=[  247],
     | 99.99th=[  342]
   bw (  MiB/s): min= 1212, max= 1390, per=100.00%, avg=1302.12, stdev=41.74, samples=120
   iops        : min= 1212, max= 1390, avg=1301.80, stdev=41.73, samples=120
  lat (msec)   : 10=0.07%, 20=10.08%, 50=49.71%, 100=38.29%, 250=1.89%
  lat (msec)   : 500=0.05%
  cpu          : usr=7.99%, sys=6.89%, ctx=22234, majf=0, minf=0
  IO depths    : 1=0.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=61.8%, >=64=38.1%
     submit    : 0=0.0%, 4=89.4%, 8=8.6%, 16=1.9%, 32=0.1%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=88.8%, 8=9.0%, 16=2.1%, 32=0.1%, 64=0.1%, >=64=0.0%
     issued rwts: total=0,78050,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=64

Run status group 0 (all jobs):
  WRITE: bw=1300MiB/s (1364MB/s), 1300MiB/s-1300MiB/s (1364MB/s-1364MB/s), io=76.3GiB (81.9GB), run=60065-60065msec

Disk stats (read/write):
  sdb: ios=51/94114, merge=0/12902, ticks=25/4408541, in_queue=4408566, util=99.89%
fill_disk: (g=0): rw=randwrite, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=libaio, iodepth=64
fio-3.28
Starting 1 process
Jobs: 1 (f=1): [w(1)][100.0%][w=1094MiB/s][w=8755 IOPS][eta 00m:00s]
fill_disk: (groupid=0, jobs=1): err= 0: pid=1809863: Fri Oct 20 12:56:54 2023
  write: IOPS=9757, BW=1220MiB/s (1279MB/s)(25.0GiB/20990msec); 0 zone resets
    slat (usec): min=5, max=1192, avg=49.62, stdev=44.31
    clat (msec): min=2, max=501, avg= 6.50, stdev= 5.26
     lat (msec): min=2, max=501, avg= 6.55, stdev= 5.26
    clat percentiles (usec):
     |  1.00th=[ 3359],  5.00th=[ 3621], 10.00th=[ 3818], 20.00th=[ 4080],
     | 30.00th=[ 4359], 40.00th=[ 4621], 50.00th=[ 4948], 60.00th=[ 5342],
     | 70.00th=[ 6063], 80.00th=[ 7635], 90.00th=[10814], 95.00th=[14091],
     | 99.00th=[27395], 99.50th=[34341], 99.90th=[52691], 99.95th=[60031],
     | 99.99th=[90702]
   bw (  MiB/s): min= 1114, max= 1361, per=100.00%, avg=1229.54, stdev=57.58, samples=41
   iops        : min= 8914, max=10890, avg=9836.29, stdev=460.67, samples=41
  lat (msec)   : 4=17.06%, 10=70.80%, 20=9.93%, 50=2.09%, 100=0.12%
  lat (msec)   : 250=0.01%, 500=0.01%, 750=0.01%
  cpu          : usr=9.96%, sys=16.87%, ctx=83346, majf=0, minf=13
  IO depths    : 1=0.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=47.3%, >=64=52.7%
     submit    : 0=0.0%, 4=93.9%, 8=5.3%, 16=0.7%, 32=0.1%, 64=0.1%, >=64=0.0%
     complete  : 0=0.0%, 4=93.6%, 8=5.6%, 16=0.8%, 32=0.1%, 64=0.1%, >=64=0.0%
     issued rwts: total=0,204800,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=64

Run status group 0 (all jobs):
  WRITE: bw=1220MiB/s (1279MB/s), 1220MiB/s-1220MiB/s (1279MB/s-1279MB/s), io=25.0GiB (26.8GB), run=20990-20990msec

Disk stats (read/write):
  sdb: ios=51/204246, merge=0/27, ticks=28/1323261, in_queue=1323288, util=99.75%
