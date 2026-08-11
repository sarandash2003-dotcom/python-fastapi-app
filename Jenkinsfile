pipeline {
  agent any

  environment {
    DOCKER_IMAGE  = "dassaran504/static-website"
    GIT_REPO_NAME = "python-flask-app"
    GIT_USER_NAME = "sarandash2003-dotcom"
  }

  options {
    timeout(time: 30, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  stages {
    stage('Checkout') {
      steps {
        sh 'echo "passed"' 
      //  git branch: 'main', url: 'https://github.com/Doom710/python-flask-app'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          def scannerHome = tool 'SonarScanner'
          withSonarQubeEnv('sonarqube') {
            sh """
              ${scannerHome}/bin/sonar-scanner \\
                -Dsonar.projectKey=flask-gitops-app \\
                -Dsonar.projectName='Flask GitOps App' \\
                -Dsonar.sources=app/ \\
                -Dsonar.language=py \\
                -Dsonar.python.version=3.11 \\
                -Dsonar.sourceEncoding=UTF-8
            """
          }
        }
      }
    }

    stage('Build and Push Docker Image') {
      steps {
        script {
          sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .'

          def dockerImage = docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}")
          docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
            dockerImage.push()
            dockerImage.push("latest")
          }
        }
      }
    }

    stage('Update Deployment File') {
       steps {
       pipeline {
    agent any

    stages {
        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
                        def dockerImage = docker.build("dassaran504/static-website:${env.BUILD_NUMBER}")
                        dockerImage.push()
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Update Deployment File') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh """
                        git config user.email "sarandash2003@gmail.com"
                        git config user.name "sarandash2003-dotcom"
                        
                        # Dynamically updates the image tag in your Kubernetes deployment file
                        sed -i 's|image: dassaran504/static-website:.*|image: dassaran504/static-website:${env.BUILD_NUMBER}|g' k8s/deployment.yaml
                        
                        git add k8s/deployment.yaml
                        git commit -m "Update flask app image tag to ${env.BUILD_NUMBER} [skip ci]"
                        
                        # Push changes back to GitHub safely using dynamic credentials
                        git push https://${GIT_USER}:${GIT_TOKEN}@://github.com HEAD:main
                    """
                }
            }
        }
    }

    post {
        always {
            // Clean workspace to free up disk space after the run finishes
            cleanWs()
        }
    }
}
