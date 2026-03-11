pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose run tests'
            }
        }

    }

    post {
        always {
            sh 'docker compose down'
        }
    }
}