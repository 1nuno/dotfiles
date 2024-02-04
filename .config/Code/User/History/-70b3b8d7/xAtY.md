#  
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



