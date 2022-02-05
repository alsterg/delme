This is a minimal implementation of the take-home test from Marshall Wace.

Questions & Answers:
1. How would you scale this script and run it with resiliency to e.g. handle 1000s of domains?
   * Start a python process per core, and using async I/O serve multiple concurrent requests.
   * Rewrite it in a more performant language, like Go or C++.
   * Scale it horizontally by implementing it as a micro service with clearly defined RPCs, with an RPC load balancer in-front.
   * Redesign the ssllib API (dependency) from a poll to a subscription model, using Web Sockets or SSE.
   * Split the service into two parts, one (application front-end - AFE) that receives the requests and places them in a work queue (e.g. RedisDB)
   * and another (backend/worker) that pickes the tasks from the queue and actually executes the http operation to ssllib.
   * the results of the operation will be reflected back in the DB, which a different AFE node can serve back to the callee 
2. How would you monitor/alert on this service?
   * Except for the standard host metrics (CPU, Mem, IO, Net, etc), I would add application specific metrics such as
       * counter for incoming & outgoing RPCs
       * latency distribution the the same
       * counters for each category of HTTP status code
       * counters for library esoteric errors (as returned by the API)
   * I would also export counters from Python VM, such as those for GC
   * Alerting:
       * In terms of alerting, I would alert on high-latency and non-2XX status codes. I would also alert on low-qps (in case the process has hanged)
       * Also on abnormal terminations of the process
       * Finally I would also alert on specific host metrics (consistently high average mem or cpu), but only with a ticket (not paging)
3. What would you do to handle adding new domains to scan or certificate expiry events from your service?
   * I would implement as a microservice with a clearly defined REST API that would allow for dynamic update of the configuration.
   * For this the script would have to be re-written as a "daemon".
   * Since the service would be horizontally scalable, the configuration would have to be written in a data store, such as Consul. An active subscription to Concul would notify all the microservies to pick up the new config.
4. After some time, your report requires more enhancements requested by the Tech team of the company. How would you handle these "continuous" requirement changes in a sustainable manner?
   * I would have to establish a CI/CD pipeline
   * I would establish alpha/beta, pre-prod, prod environments.
   * Any changes should be backward compatible
   * Any changes should be pushed progressively accross the environments, and gradually within the same environment
   * Any change should be monitored for regression
