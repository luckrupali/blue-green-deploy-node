# Blue-Green Deployment Strategy using Python and AWS

This project showcases a real-world implementation of **Blue-Green Deployment** for an AWS RDS instance using **Python automation (Boto3)** and **Lambda-compatible scripts**.

It automates:
- Creation of a new green environment
- Switchover from blue to green
- Deletion of old blue environment

---

## 🎯 Use Case

To achieve **zero-downtime upgrades** and **cost-efficient scaling**, we implemented a Blue-Green Deployment pattern using AWS RDS Blue/Green features and automated the workflow through Python.

This was used in a production scenario where:
- High read workloads required scaling
- Instance type switching helped reduce cost
- Green environments were tested before full switchover

---

## 🛠️ Tools & Technologies

- 🐍 Python (Boto3)
- 🟦 AWS RDS (Blue/Green Deployment)
- 📘 AWS SSM (Parameter Store)
- 📊 CloudWatch (Monitoring)
- 🧠 Lambda-compatible logic

---

## 🗂️ Folder Structure
blue-green-deploy-node/
├── scripts/
│ ├── create_green_env.py # Create green RDS environment with optimized config
│ ├── switchover_to_green.py # Trigger switchover from blue to green
│ └── delete_old_blue_env.py # Clean up old blue environment after switchover
├── README.md


---

## ⚙️ Script Descriptions

### 1️⃣ `create_green_env.py`
Creates a new green environment based on the current RDS instance:
- Copies existing config dynamically
- Applies new instance class or storage tuning
- Saves deployment identifier in AWS SSM

### 2️⃣ `switchover_to_green.py`
Triggers a safe switchover:
- Fetches the latest deployment
- Converts time objects for logging
- Initiates switchover programmatically

### 3️⃣ `delete_old_blue_env.py`
Performs post-switchover cleanup:
- Deletes the old (blue) DB instance
- Removes the deployment after switchover completes

---

## 🔐 Security Notes

- This repo contains no hardcoded credentials or sensitive AWS info.
- Make sure to configure your AWS credentials securely (e.g. IAM role, CLI config, or Lambda execution role).

---

## 💡 Outcome

- ✅ Achieved **zero-downtime deployments**
- ✅ Reduced manual effort using automation
- ✅ Saved 40–50% on RDS costs by scaling with green environments
- ✅ Simplified rollback/testing by keeping blue alive until green was proven

---

## 👩‍💻 Author

**Rupali Lakkewar**  
[LinkedIn](https://linkedin.com/in/rupali-lakkewar) | [GitHub](https://github.com/luckrupali)

---

## 📌 Notes

You can integrate this with a CI/CD system, or trigger from Lambda as part of your release pipeline.

---

