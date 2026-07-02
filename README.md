# Build on Trainium

A landing page for getting started with Build on Trainium.

## Getting started

> _TODO: short intro — who this is for, what you'll need (AWS account, region, access)._

## Increasing your vCPU limit

When you need to increase your vCPU limit, go to this link: https://pulse.aws/survey/B2D7WSLE?p=0

## How to launch a Trn2 capacity block

This guide walks through how to launch a Trn2 instance using **Capacity Blocks for ML**.

### Step 1 — Open the AWS Console
Go to https://us-west-2.console.aws.amazon.com/

### Step 2 — Select the correct Region
- We recommend starting with **trn2.3xl in Melbourne** (ap-southeast-4).
- If you're working with a model larger than **30B**, switch the Region to **Ohio** (us-east-2).

### Step 3 — Open EC2
Search for **EC2** in the top search bar and click it.

### Step 4 — Go to Capacity Reservations
From the EC2 dashboard, click **Capacity Reservations** in the left-hand menu.

### Step 5 — Create a Capacity Reservation
Click the orange **Create capacity reservation** button in the top right.

### Step 6 — Choose Capacity Block for ML
Select **Capacity Block for ML** on the right.

### Step 7 — Select the instance type
Choose **trn2.3xl**.

### Step 8 — Find capacity
Click **Find capacity**.

### Step 9 — Pick your capacity block
Select the time window (24-hour block) that fits your needs — you can launch **same day** or **next day** — then click **Create** in the bottom right.

### Step 10 — Open your reservation
Once your capacity reservation is ready, return to the **Capacity Reservations** tab on the left and click your reservation.

### Step 11 — Launch an instance
Click the orange **Launch instance** button in the top right.

### Step 12 — Name it and search for the AMI
- Give the instance a name (e.g., `test`).
- In the AMI search box, type **neuron** and press search.

### Step 13 — Select the Neuron Deep Learning AMI
After typing **neuron** and pressing search, select one of the Deep Learning AMIs:
- **Deep Learning AMI Neuron (Amazon Linux 2023)**, or
- **Deep Learning AMI Neuron (Ubuntu 24.04)** — whichever you prefer.

### Step 14 — Configure key pair and storage
- Create your own **key pair** (you'll need the `.pem` file to connect).
- Increase storage to the size you need (e.g., **1000 GB**).
- Click the orange **Launch instance** button on the right.

### Step 15 — Open Instances
Click **Instances** to see your new instance.

### Step 16 — Connect
Select the instance and click **Connect**.

### Step 17 — SSH in
Open the **SSH client** tab and copy the example SSH command. Run it, and you're in.

### Step 18 — Verify Neuron devices
Run:

```bash
neuron-ls
```

You should see output like this:

```
instance-type: trn2.3xlarge
instance-id: i-xxxxxxxxxxxxxxxxx
logical-neuroncore-config: 2
+--------+--------+----------+--------+--------------+----------+------+
| NEURON | NEURON |  NEURON  | NEURON |     PCI      |   CPU    | NUMA |
| DEVICE | CORES  | CORE IDS | MEMORY |     BDF      | AFFINITY | NODE |
+--------+--------+----------+--------+--------------+----------+------+
| 0      | 4      | 0-3      | 96 GB  | 0000:33:00.0 | 0-11     | 0    |
+--------+--------+----------+--------+--------------+----------+------+
```

That confirms the Neuron devices are visible and the instance is ready to use.

## How to invite your students

> _TODO: step-by-step guide for giving students access._
>
> 1. _TODO: Decide the access model (IAM users, IAM Identity Center, or separate accounts)._
> 2. _TODO: Create accounts / users for each student._
> 3. _TODO: Assign permissions (least-privilege policy for launching/using instances)._
> 4. _TODO: Share onboarding instructions and the vCPU survey link above._
> 5. _TODO: Set up cost controls / budgets per student or group._

## Model examples

A collection of Neuron model examples lives here: https://github.com/arminagha1234/Armin-Neuron
