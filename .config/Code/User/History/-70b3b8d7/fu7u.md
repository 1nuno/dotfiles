# Pages to impress

stuff about networking

DC Storage - 20 - 33

# cloud computing

## service delivery model

### SaaS

- The consumer can use the provider's application running on a cloud infrastructure;

- The consumer does cannot control the following:
    0. Underlying cloud infraestructure
    1. Network
    2. Servers
    3. Operating systems
    4. Storage
    5. Individual application capabilities with the possible exceptions of some user specific application configuration settings.

### PaaS

- The consumer can use use the providers service to deploy its own application

- The consumer cannot control the following
    0. Underlying cloud infraestructure
    1. Network
    2. Servers
    3. Operating systems
    4. Storage

- The consumer can control the following:
   1. The deployed application
   2. Possibily the application hosting environment

### IaaS     

- The consumer cannot control:
    0. Underlying cloud infraestructure

- The consumer can control:
    1. some network componets like nthe host firewall for example
    2. operating systems
    3. storage
    4. deployed applications


## Cloud deployment models

### Public

- More elasticity
- Less CAPEX
- Less customizability
- Less Security
- Access from outside the firewall
- High standarization
- usually on a pay per use basis
- exists on and of premises

### Private

- Less elasticity
- More CAPEX
- More customizability
- Access from inside the firewall
- Low standarization
- More secure than a public deployment model
- Exists on and of premises

### Community cloud

- Its a mix of benefits and disavantages from the private and public cloud

### Hybrid cloud

- Advantages of both Private and Public cloud
- Demand peak management
- Data recovery scenarios
- Theres a conflict of interest problems where usually public cloud providers make it hard to integrate technologies outside of their ecossystem. Its better for them if you just use all of the services they provide out of the box.


## The 5 main attributes of cloud computing

### ON Demand

A consumer can unilaterally provision computing capabilities without requiring human interaction with the service provider.


### Broad Network Access

The services must be available to anyone with an internet connectin anywhere and anytime


### Resorce Pooling

The provider's computing resources, physical and virtual are pooled together using a multi-tenant model assigning these resorces dynamically depending on user demand.

The multi-tenancy is having different consumers consuming the same hardware in a isolated way without them knowing the existence of one another.

### Rapid Elasticity

The consumer must be able to increase or decrease the computing capabilities on demand.

This is possible through horizontal scaling (in/out scaling) which focus on adding more nodes (machines) to the existing setup, but to do this, it is important that the application supports multiple servers and the complexity of a distributed application may impose growth limits.


Another way of achieving elasticity is through vertical scaling (up/dow) which focus on ugrading the existing nodes; For example increase the CPU and Memory storage of the machine. In order for this method to work the operating system must support dynamic resizing of the computing resources. Some operating systems might impose scalability boundaries (e.g., maximum supported number of CPU's and etc).

### Mesureability

Every single resource usage must be mesured in a comprehensible way in order to increase the transparency between the consumers and providers.

## Some Roles in Cloud Computing

- cloud service provider
- cloud service owner
- cloud consumer
- cloud administrator
- etc


# Virtualization

Virtualização é um método usado para esconder as caracteristicas físicas dos recursos computacionais, da maneira como os mesmos interagem com outros sistemas, aplicações ou end users com o objectivo de fazer uma única máquina parecerem várias ou vice-versa.


## Virtual machines

Virtual machines are software based execution environments that supports the execution of code as if it were a physical machine. Virtual machines can assume 2 types: Process virtual machines and System virtual machines.

### process virtual machines

This type of virtual machine is installed on top of a Operating system and offers a uniform execution environments for specific applications. A well know example is the JVM, Java Virtual Machine.

### System Virtual Machines

This type of virtual machine allow us to multiplex our hardware resources between multiple operating systems. Some characteristics are:

- The same hardware might have a number of different vm's each running different os's
- Each vm on the hardware is isolated from the others
- The hardware itself can be virtualized, meaning that the specificities of the hardware that the vm sees does not necessarily correspond to the actual hardware specs.
- A software controls the operation of the VM's and that software is called: Hypervisor or VMM (Virtual Machine Monitor)


### types of hypervisors

The hypervisors can be classified in 2 main types:

- **type II** - the hypervisor is on top of an existing operating system
- **type I** - the  hypervisor is directly on top of the hardware 


## types of virtualization

### para virtualization

This type of virtualization happens when we modify the VM's OS so it starts using the hypervisor services instead of direct hardware resources. The problem with this approach is that it demands explicit support fromt the hosted OS and not all OS's support this. Both the hypervisor and the OS share the ring 0 and the OS makes hypercalls to the VMM to execute non-virtualizable OS instructions.

### full virtualization

Unlike the para virtualization, the full virtualization doesn't require the OS to natively support communicating with a hypervisor. The way this virtualization works is by having the OS "live" in ring 1. The problem is that most OS's are designed to inhabit ring 0 and when we put it on ring 1 the semantics behind some instructions change and to solve this the VMM performs a binary translations of those instructions in order to interpret and execute them.

### hardware assisted virtualization

As the name suggests this virtualization type depends on the support of the hardware itself. When using this virtualization the hypervisors stays in a new ring below ring 0, which eliminates the necessity of binary translation; Instead the OS requests are trapped directly to the VMMj


## Benefits from virtualization

### Server consolidation

Using the classic paradime with no virtualization, servers where shown to use 10 to 20 percent less then their max capacity which is extremely wastefull. With virtualizaton we are able to maximize the use of each individual server which results in multiple benefits such as:

- less CAPEX;
- less money spent on space ocuppied by the server;
- less money spent on the energy spent by the servers;
- less money spent on the cooling system for the servers.

### The use of legacy systems

Some legacy systems require old hardware that is no longer manunfactured and virtualization can make these systems usable with recent hardware technology.

### Enhanced availability

Virtualization allows us to take snapshots of our system which create the possibility of doing rollbacks in case of any type of failure.

### Live migration

1. Source hypervisor establishes a connection with the target Hypervisor
2. Target hypervisor creates a new gues vCPU and etc
3. Source hypervisor sends all the read only files
4. Source hypervisor sends all the clean read write files
5. Repeat step 4 because some read write files might have been altered and are marked as dirty.
6. As this cycle becomes very short, the source VMM freezes, sends the vCPU final state, other details and the final dirty files to the target VMM and tells it to start running the guest.
7. Once the target acknowledges guest running, source terminates its guest.

### Isolation of Services/Application

We need not to keep similar services running on the same server. Each VM becomes specialized in a single service which reduces both the security and failure risks that can result between the interaction of two distinct services.

### Standarization

It becomes possible to tune aplications/services for a specific reference platform indepently of available hardware. For instance at a company level the sys admin might define that all services will use linux.


# Network Virtualization

i have no idea how this sht works

# DC storage

## Raids

### Raid 0

- data is striped across all disks
- no fault tolerance
- used in situations where we can afford to lose some data and we need high writing and reading speeds (for example video streaming)

### RAID 1

- data from a disk is completely mirrored to another disk;
- has fault tolerance as we can recover the data in case a disk fails;
- the recover times are fast;
- used in critical situations where we cannot afford to lose data
- duplication of data makes it so that we can only use half of our available space to store data

### RAID 1 + 0

- Data is first mirrored and then both copies of the data are striped across hdds in a raid set.
- Used in databases that require high I/O, random access and availability

### RAID 3

- In this raid the concept of parity is introduced which means that we reserve one disk to store information that allows us to reconstruct another disk in case of failure;
- The stripe is performed at byte-level
- Requires syncronicities between the disks for good performance
- Used in situations where we need to access data sequentially such as video streaming;

### RAID 4

- Same thing as raid 3 with the only difference that Raid 4 striping is performed at block level which means that data disks can be accessed independently which means that specific data elements can be read or writen on a specific disk without the need to perform striping.

### RAID 5

- As opposed to RAID 4 and RAID 3 where the parity info was stored on a single disk, in RAID 5, that information is distributed along all disks which helps us to overcome write bottlenecks;

### RAID 6

- Same as RAID 5 but instead of one parity we have two, which allows us to recover up to 2 disks in case of failure of both of them.

### Hotspare

- This is an extra HDD that sits in idle with the rest of the others. Once one of the disks has a failure, this hotspare is used to replace it. Once the failed drive is replaced, the hotspare is added permanently or we can copy the hotspare data into the new hdd and make it return to its idle state.

## Inteligent Storage Systems

### Front-end

The front end is composed by controlers and ports:

- the ports allows hosts to connect to the system using the appropriat transport protocol for storage connections;

- the controlers routes the data to and from the cache via the internal data bus. When cache receives the data controller acknowledges. Controlers are also responsible for optimizing I/O processing by using command queuing algorithms which is a technique to determine the order of executions of received commands in order to reduce drive head movements and improve disk performance.

### Cache

write through cache - the data is written to the cache and then to the disk and only then the acknowledgement is sent.

write back cache - the data is written to the cache, the acknowledgement is sent and after a period the data in the cache is written to the disk

cache failure on read - no problem the data is on the disk

cache failure on write - we have two ways of dealing with it:

cache mirroring - we store the cache in two different memory locations which means that if theres a failure we have a backup. This introduces the problem of cache coherence because now we need to make sure those two caches are syncronized

cache vaulting - in the case of power failure, use the battery power to write the cache content to the disk.

### Backend

- The controlers are used to comunicate with the disks for writes and reads; the back end controlers implements features such as error detection and correction; limited and temporary data storage.

- The disks connect to the backend through the ports;

- To deal with load balancing and we usually have multiple controlers and dual ported disks.

### Physical disks

- Disks connected to the back end
- Typical interfaces: SCSI and Fibre Channel, SATA.

## LUNs - Logical Unit Number

Physical drives or groups of Raid protectes drives can be logically split into volues. A Lun is a way to uniquely identify each one of those volumes.

## DAS - Directly attached storage

