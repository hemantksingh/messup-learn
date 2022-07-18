# AWS

## EC2 Instance

You can launch an EC2 instance from the AWS console with the default settings: Amazon Linux, t2.micro and download the private key for connecting to the EC2 instance via ssh

```sh
# SSH to the ec2 instance
chmod 400 ~/Downloads/ec2_rsa.pem
ssh ec2-user@<instance-publicip> -i ~/Downloads/ec2_rsa.pem

# post ssh login
       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/
[ec2-user@ip-172-31-5-104 ~]$

# install apache
sudo su
yum update -y
yum install -y httpd
systemctl start httpd
# automatically get it to start on boot 
systemctl enable httpd
systemctl status httpd

# add a webpage
echo '<html><head><title>AWS Solution Architect!</title></head><body><h1>Who is an AWS Solution Architect?</h1><iframe width="560" height="315" src="https://www.youtube.com/embed/Js21xKMFdww" frameborder="0" allowfullscreen></iframe></body></html>' > /var/www/html/index.html
```

Provided you have configured HTTP in your security groups and allowed internet connectivity within your subnet and NACL, you can visit the above webpage by going to the public IP of your EC2 instance.

### EC2 instance metatdata

You can [retrieve the EC2 instance metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html) by querying a predefined URL.

e.g.

```sh
# list endpoints
curl http://169.254.169.254/latest/meta-data/

# get instance IP
curl http://169.254.169.254/latest/meta-data/public-ip4

# get bootstrap script that was run when the instance was provisioned
curl http://169.254.169.254/latest/user-data
```

### Virtual Networking Options

* ENI Elastic Network Interface: For basic, day-to-day networking
* EN Enhanced Networking: Uses single root I/O virtualization (SR-IOV) to provide high performance networking between 10 Gbps - 100 Gbps
* EFA Elastic Fibre Adapter: Accelerates High performance Computing (HPC) and machine learning applications

### Storage

AWS uses Elastic Block Store (EBS) storage volumes to attach to EC2 instances. These are **virtual hard disks** which can be used in the same way you would use any system disk for:

* Creating a file system
* Run a database
* Run an operating system
* Install applications

You need a minimum of 1 volume per EC2 instance. This is called the [root device volume](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/RootDeviceStorage.html) where your operating system is installed and it contains the [AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) (Amazon Machine Image - blueprint for an EC2 instance) used to boot the system. AMIs can be backed by EBS or instance store. Instance store volumes are ephemeral and cannot be stopped. If the underlying host fails you will lose your data. EBS backed instances can be stopped and the data on this instance is persistent.

**Snapshots** are a point-in-time copy (a photograph) of a volume that exist on S3. Snapshots are incremental meaning only the delta since the last snapshot is moved to S3. This saves dramatically on space and the time it takes to take the snapshot. Therefore the first snapshot can take considerably longer.

EBS Volume Types

* General Purpose SSD (gp2, gp3) - suitable for boot disks and general applications
* Provisioned IOPS SSD (io1 or io2) - for low latency OLTP workloads
* Throughput Optimized HDD (st1) - for large datasets, datawarehouses and ETLs, cannot be a boot volume
* Cold HDD - for less frequently accessed data like file servers, cannot be a boot volume

EBS volumes will always be in the same AZ as EC2, are replicated within a single AZ to protect against hardware failures. They are dynamically scalable to increase capacity and change the volume type (e.g. go from gp2 to io2) with no downtime or performance impact to your live systems. However you will need to extend the filesystem in the OS so that it can see the resized volume.

#### Migrating an EC2 instance from one region to another

* Create a snapshot or use an existing snapshot of the volume
* Copy the snapshot to the target region (You can decide to encrypt the snapshot if it was from an unencrypted volume)
* Make an Amazon Machine Image (AMI) from the snapshot
* Launch an instance from the AMI
