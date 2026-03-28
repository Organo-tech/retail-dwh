Hey, checked the repo. The table structure looks correct, but the current implementation isn't production-ready yet and misses several engineering best practices.

### **New Rule: Git Workflow**
1. No more pushing directly to main. 
2. Do NOT use the "Upload files" button on the GitHub website.
From now on, you must use Git commands via Terminal for everything.
  - Create a new branch (e.g., feature/fix-docker-compose) using git checkout -b ...
  - Do your work and commit locally.
  - Push the branch to remote using git push ...
  - Open a Pull Request (PR) on GitHub and add me as the reviewer.
I want to review your code properly before it merges.
**Do your own research on using Git at a production level**. Be thorough, even your commit messages must follow a standard convention

### **Your Mission Checklist**
**1. Docker Reliability & Ops** 
Your docker-compose is currently fragile. Let's make it robust.

- [x] Fix Portability: You used a Windows path (D:/...) for volumes. This breaks the code on Linux/Mac. Change it to a relative path (e.g., ./data). -> remember docker advantage? PORTABLE
- [x] Add Healthchecks: The orchestrator doesn't know if Postgres is actually ready to accept connections. Add a healthcheck 
- [x] Restart Policy: If the container crashes, it stays dead. Add a restart policy 
- [x] Resource Limits: Your container can consume the entire host's RAM/CPU. Add deploy.resources limits to be safe.
- [x] Config Tuning: Mount a custom postgresql.conf to tune shared_buffers and max_connections.
**you should comment each of the docker compose configurations and explain what is the purpose of that configurations**

**2. Fix the Security**  
Right now your DB password is hardcoded in the docker-compose file. That's a security risk.
- [x] Move all credentials (user, pass, db name) to a environment variable file
- [x] Update docker-compose.yml to read variables from that file.
- [x] Crucial: Add .env to your .gitignore so you don't accidentally upload secrets to GitHub.

**3. Optimize the Database** 
Imagine if the data grows to 1 million rows. Your joins will be slow.
- [x] Add Indexes to your Foreign Key columns.
- [x] Run EXPLAIN ANALYZE on your query to see the difference.
**you're also allowed to do another database optimizations method, also put the optimization script in this repo ya**

**4. Level Up Data Quality Manual SQL checks are tedious. Let's automate it.**
- [x] Install Great Expectations (use docker)
- [x] Create a simple suite to check the Fact table (e.g., ensure IDs are not null, price is not negative).

**5. Access Control (RBAC)** 
Never use the root user for reporting tools.
- [ ] Create a new Postgres user (e.g., bi_viewer) that only has SELECT (read-only) permission.

**6. Build a 'Mart' Layer** 
Dashboards shouldn't query raw tables directly (it's heavy).
- [ ] Create a new schema called mart.
- [ ] Create a pre-aggregated table/view (e.g., mart.monthly_sales) that joins the Fact + Dims for easier reporting.

**7. Visualize it (Apache Superset)**
- [ ] Add Apache Superset to your docker services.
- [ ] Connect it using the bi_viewer user you created before.
- [ ] Build 1 simple dashboard using data from the mart layer.

**You have until next Wednesday to complete this. If you finish early, don't just stop, use the extra time to polish and optimize the project. Make sure what you deliver on Wednesday is your best work.**
