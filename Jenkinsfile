def imageName = "example-pipeline"
def tagName = "0.0.1"


pipeline {
	agent any

	environment {
		AWS_ACCOUNT_ID = credentials("AWS_ACCOUNT_ID")
        AWS_ACCESS_KEY_ID = credentials("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = credentials("AWS_SECRET_ACCESS_KEY")
		IMAGE_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/${imageName}:${tagName}"
	}

	stages {
		stage("Checkout") {
			steps {
				checkout scm
				sh "aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com"
			}
			post {
				success {
                    echo "The Checkout stage successfully."
                }
                failure {
                    echo "The Checkout stage failed."
                }
			}
		}

        stage("Main pipeline") {
			failFast true
			parallel {
				stage("Update Images") {
					stages {
						stage("Build Image") {
							steps {
								dir('./ecrpush')
								script{
                                    sh "docker build -t ${imageName}:${tagName} ."
								}
							}
							post {
								success {
									echo "The Build Image stage successfully."
								}
								failure {
									echo "The Build Image stage failed."
								}
							}
						}
						stage("Tag an Push Image") {
							steps {
								script {
									sh "aws ecr describe-repositories --repository-names ${imageName} || aws ecr create-repository --repository-name ${imageName}"
									sh "docker tag ${imageName}:${tagName} ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/${imageName}:${tagName}"
									sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/${imageName}:${tagName}"
								}
							}
							post {
								success {
									echo "Tag and Push Image stage successfully."
								}
								failure {
									echo "Tag and Push Image stage failed."
								}
							}
						}
						stage("Clean Image") {
							steps {
								script {
									sh "docker rmi -f ${imageName}:${tagName} ${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/${imageName}:${tagName}"
								}
							}
							post {
								success {
									echo "The Clean Image stage successfully."
								}
								failure {
									echo "The Clean Image stage failed."
								}
							}
						}
					}
				}
                stage("Update Application") {
                    /* other service */
                }
			}
		}
    }
}