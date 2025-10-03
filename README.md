MERN with Microservices


This project simulates a production-grade cloud-native deployment workflow, showcasing how modern DevOps practices enable scalable, automated, and reliable application delivery on AWS

Use Case

Build and deploy a containerized MERN application with separate microservices (frontend, hello service, profile service). Implement CI/CD pipeline using Jenkins to automate Docker image builds and push them to Amazon ECR. Use Infrastructure as Code (IaC) with Python (Boto3) to provision AWS infrastructure (VPC, Subnets, Security Groups, Auto Scaling Groups, Load Balancer). Deploy services on EC2 instances with Docker managed by Auto Scaling Groups. Route traffic through an Application Load Balancer (ALB) with health checks. Enable monitoring & logging via Amazon CloudWatch.



🛠️ Tools & Technologies

AWS: EC2, ECR, ALB, ASG, VPC, Route 53, CloudWatch, IAM DevOps: Jenkins, Docker, Boto3 (Python), Infrastructure as Code Application Stack: MERN (MongoDB, Express.js, React, Node.js) Version Control: GitHub



Detailed Folder Structure (with explanations)


SampleMERNwithMicroservices/

│
├── backend/
│   ├── helloService/        # Microservice 1 (Hello API)
│   ├── profileService/      # Microservice 2 (Profile API)
|   |── README.md/           # Backend documentation


│
├── frontend/                # React-based frontend
│
├── iac_alb.py               # IaC script to create ALB + Target Groups
├── iac_asg.py               # IaC script to create ASG + Launch Templates
├── iac_infra.py             # IaC script to create VPC, Subnets, SG
|── README.md                # Backend documentation
│
├── Jenkinsfile              # CI/CD pipeline definition
├── README.md                # Main documentation
└── screenshots/             # Folder for architecture/setup screenshots



Deployment Workflow Diagram
         Developer Commit
                │
                ▼
          Jenkins Pipeline
                │
       ┌────────┴────────┐
       ▼                 ▼
 Docker Build        Docker Push
(local/EC2)           to Amazon ECR
                │
                
                ▼
     Infrastructure as Code (Boto3)
                │
       ┌────────┴────────┐
       ▼                 ▼
   Auto Scaling      Application
     Groups          Load Balancer
   (EC2 + Docker)     (ALB + TGs)
       │
       ▼
       
   Frontend + Backend Services
   (Accessible via ALB DNS)

For helloService, create .env file with the content:

PORT=3001

For profileService, create .env file with the content:

PORT=3002

MONGO_URL="specifyYourMongoURLHereWithDatabaseNameInTheEnd"
Finally install packages in both the services by running the command npm install.


For frontend, you have to install and start the frontend server:
cd frontend
npm install
npm start
Note: This will run the frontend in the development server. To run in production, build the application by running the command npm run build
