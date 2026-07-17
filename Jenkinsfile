pipeline {
    agent any

    environment {
        AWS_REGION = "ap-southeast-2"
        AWS_ACCOUNT_ID = "150100906571"

        FRONTEND_REPO = "employee-frontend"
        BACKEND_REPO = "employee-backend"

        FRONTEND_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${FRONTEND_REPO}:latest"
        BACKEND_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${BACKEND_REPO}:latest"
    }

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('backend') {
                    sh 'docker build -t employee-backend .'
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                dir('frontend') {
                    sh 'docker build -t employee-frontend .'
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-creds',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin \
                    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                docker tag employee-backend:latest $BACKEND_IMAGE
                docker tag employee-frontend:latest $FRONTEND_IMAGE
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                docker push $BACKEND_IMAGE
                docker push $FRONTEND_IMAGE
                '''
            }
        }

        stage('Deploy Backend') {
            steps {
                sh '''
                docker stop backend-container || true
                docker rm backend-container || true

                docker pull $BACKEND_IMAGE

                docker run -d \
                  --name backend-container \
                  -p 8000:8000 \
                  $BACKEND_IMAGE
                '''
            }
        }

        stage('Deploy Frontend') {
            steps {
                sh '''
                docker stop frontend-container || true
                docker rm frontend-container || true

                docker pull $FRONTEND_IMAGE

                docker run -d \
                  --name frontend-container \
                  -p 80:80 \
                  $FRONTEND_IMAGE
                '''
            }
        }

    }

    post {

        success {
            echo "======================================="
            echo " Deployment Completed Successfully "
            echo " Frontend : http://15.134.88.89"
            echo " Backend  : http://15.134.88.89:8000"
            echo " Swagger  : http://15.134.88.89:8000/docs"
            echo "======================================="
        }

        failure {
            echo "======================================="
            echo " Pipeline Failed"
            echo " Check Jenkins Console Output"
            echo "======================================="
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}
