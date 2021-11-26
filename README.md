# Manage AWS VPC & EC2 using Python with Boto3
---

## Project Overview

- Objective : AWS solution to manage EC2 & VPC using Python with Boto3

Plan, configure, deploy and operate AWS cloud solution

---
## Requisites 

- AWS Account
- Python IDE : Pycharm

---
## Development Tools & Environment

- AWS CLI
  To configure our environment with credentials

- Python
  Language to interact with AWS
  
- PyCharm
  IDE for python Development
  
- Boto3
  AWS library backed by Amazon itself
  
- OS
  To prepare our environment with Windows/Macos/Linux

---
## Architechture


<img src="https://github.com/SidSolanki28/AWS-Project-01/blob/master/Images/Architechture.PNG">


---
## Created:

* VPC
* Internet Gateway (IGW)
  - Attached IGW to VPC

* Public Subnet
* Route Table for Public Routes
  - Added IGW Route to Route Table
  - Associated Public Subnet with Public Route Table
  - Allowed IP Auto- assign on Public Subnet
* Private Subnet

* Key Pair
* Security Group
* Startup Script for public ec2 instance
  - Launched a Public EC2 instance in Public Subnet
  - Verified that our script worked by connecting to public ec2 instance
  - Access our hosted web page on Public EC2 instance
  - Launched a Private EC2 instance in Private Subnet
  - Verified connection not possibe to private ec2 instance except from witing subnet

* Descibe EC2 instances
* Modify EC2 instances
* Start EC2 instances
* Stop EC2 instances
* Terminate EC2 instances

---
## Output


<img src="https://github.com/SidSolanki28/AWS-Project-01/blob/master/Images/output.PNG">



