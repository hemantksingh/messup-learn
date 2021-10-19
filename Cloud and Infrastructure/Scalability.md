# Scalability

Systems that are expected to grow over time need to be built on top of a scalable architecture. Such an architecture can support growth in users, traffic, or data size with no drop-in performance. It should provide that scale in a linear manner where adding extra resources results in at least a proportional increase in ability to serve additional load. Growth should introduce economies of scale, and cost should follow the same dimension that generates business value out of that system. While cloud computing provides virtually unlimited on-demand capacity, your design needs to be able to take advantage of those resources seamlessly. There are generally two ways to scale an IT architecture: vertically and horizontally.

## Vertical Scaling

Scaling vertically takes place through an increase in the specifications of an individual resource, such as upgrading a server with a larger hard drive or a faster CPU. With Amazon EC2, you can stop an instance and resize it to an instance type that has more
RAM, CPU, I/O, or networking capabilities. This way of scaling can eventually reach a limit, and it is not always a cost-efficient or highly available approach. However, it is very easy to implement and can be sufficient for many use cases especially in the short term.

## Horizontal scaling

Historically load balancers have been deployed as hardware on the edge in the data centre. Hardware load balancers like Citrix NetScalar Application Delivery Controller (ADCs) and F5 require proprietary, rack-and-stack hardware appliances. In order to scale, network load balancer hardware is typically over provisioned — in other words, they are sized to be able to handle occasional peak traffic loads. In addition, each hardware device must be paired with an additional device for high availability in case the other load balancer fails. This means that most load balancers stay idle until peak traffic times.

With a shift in cloud native and microservices architecture running on dynamic runtimes like kubernetes, the supporting application infrastructure needs to be more programmable and maintainable by cross functional teams. Software load balancers bridge the divide between NewOps and DevOps, they are simply installed on standard virtual machines. [Haproxy](./Haproxy.md) and [Nginx](./Nginx.md) can both be used for load balancing your workloads across application servers.