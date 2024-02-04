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

When we think about virtualization, these are usually the virtual machines that come to mind, they allow us to multiplex our hardware resources between multiple operating systems. Some characteristics are:

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

