pipeline {
    agent any

    environment {
        DOCKER_USER = "jampallykeerthi"
        IMAGE_NAME = "url-click-analytics"
        IMAGE_TAG = "v1"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // ✅ Fetch code from GitHub using Jenkins credentials
                git branch: 'main',
                    url: 'https://github.com/jampallykeerthi/casestudy.git',
                    credentialsId: 'github-credentials'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    echo "Logging in to Docker Hub..."
                    // ✅ Use manual credentials (for testing only)
                    sh "echo 'Keerthi@88' | docker login -u '${DOCKER_USER}' --password-stdin"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing image to Docker Hub..."
                    sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying application to Kubernetes..."
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl apply -f service.yaml"
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline executed successfully — application deployed to Kubernetes!'
        }
        failure {
            echo '❌ Pipeline failed. Check the console log for details.'
        }
        always {
            echo 'Pipeline completed.'
        }
    }
}
