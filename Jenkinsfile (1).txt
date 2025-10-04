pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "us-west-2"   
        ACCOUNT_ID = "975050024946"    
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'JigarGit', url: 'https://github.com/JigarMalam/SampleMERNwithMicroservices.git'
            }
        }

        stage('Login to ECR') {
            steps {
                withAWS(credentials: 'AWScred', region: "${AWS_DEFAULT_REGION}") {
                    sh """
                      aws ecr get-login-password --region ${AWS_DEFAULT_REGION} \
                        | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
                    """
                }
            }
        }

            stage('Build & Push Docker Images') {
            steps {
                script {
                    def services = [
                        [name: "jigar-hello-service", path: "backend/helloService"],
                        [name: "jigar-profile-service", path: "backend/profileService"],
                        [name: "jigar-frontend-hp", path: "frontend"]
                    ]

                    for (svc in services) {
                        sh """
                          echo "Building image for ${svc.name} from ${svc.path}"
                          docker build -t ${svc.name}:$IMAGE_TAG ${svc.path}
                          docker tag ${svc.name}:$IMAGE_TAG ${ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${svc.name}:$IMAGE_TAG
                          docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${svc.name}:$IMAGE_TAG
                        """
                    }
                }
            }
        }
    }
}
