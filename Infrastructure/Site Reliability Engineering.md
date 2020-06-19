# Site Reliability Engineering (SRE)

Some things that an SRE could be dealing with on a given day:

* DDOS attack - Forces you to have a higher capacity than required.
* Upgrading the firmware on your router - major risk to your service.
* Use Load balancing as a means to build reliable systems.

### Google Cloud Load Balancer (GCLB)

GCLB provides a global IP address but your request still gets served from the closest location. It uses **geolocation** to serve the user with content closest to them.

* Drain & rollback to mitigate issues-
  Changing permissions on a file to fix an issue. You need to know the original permissions in order to rollback.

* Post-mortems - Come up with action items based on facts rather than blame, that can help prevent detect & mitigate outages.

* Pre-mortems

### Customer Reliability Engineering (CRE)

Come up with Service Level Objective (SLO). As long as your availability as we measure it is above your SLO, you're clearly doing a good job. You're making accurate decisions about how risky something is, how many experiments you should run, and so on. So knock yourselves out and launch whatever you want. We're not going to interfere. And this continues until you blow the budget.


CRE analogy - Entry to a free gym, where you get a fitness instructor who helps you build the muscles to cope with outages.

* Good error budget and an SLO can reduce the tension between development and operations.