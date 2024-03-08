def imageName = "example-pipeline"
def tagName = "0.0.1"


pipeline {
	agent any

	environment {
		    AWS_ACCOUNT_ID = credentials("AWS_ACCOUNT_ID")
			AWS_ACCESS_KEY_ID = credentials("AWS_ACCESS_KEY_ID")
			AWS_SECRET_ACCESS_KEY = credentials("AWS_SECRET_ACCESS_KEY")
			SUBNET_ID = credentials("SUBNET_IDS")
			SECURITY_GROUP_ID = credentials("SECURITY_GROUP_ID")
			TASK_FAMILY = "shine-s3rds"
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
		stage("Build Image") {
            steps {
                // GitHub에서 코드를 가져오면서 ecrpush 디렉토리로 이동하고 해당 디렉토리에서 Dockerfile을 사용하여 도커 이미지 빌드
                checkout([$class: 'GitSCM',
                          branches: [[name: 'main']],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [[$class: 'SubmoduleOption', recursiveSubmodules: false]],
                          submoduleCfg: [],
                          userRemoteConfigs: [[url: 'https://github.com/dnddl6962/final_project.git']]])

                dir('ecrpush') {
                    script {
                        sh "docker build -t ${imageName}:${tagName} ."
                    }
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

        stage("Main pipeline") {
			failFast true
			parallel {
				stage("Update Images") {
					stages {
						// stage("Build Image") {
						// 	steps {
						// 		script {
                        //             sh "docker build -t ${imageName}:${tagName} ."
						// 		}
						// 	}
						// 	post {
						// 		success {
						// 			echo "The Build Image stage successfully."
						// 		}
						// 		failure {
						// 			echo "The Build Image stage failed."
						// 		}
						// 	}
						// }
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
						stage("Update ECS Task Definition") {
							steps {
								script {
									def taskDefinition = """
									{
									"family": "${TASK_FAMILY}",
									"containerDefinitions": [
										{
										"name": "${imageName}",
										"image": "${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/${imageName}:${tagName}",
										"cpu": 256,
										"memory": 512,
										"essential": true
										}
									]
									}
									"""

									sh "echo '${taskDefinition}' > taskDefinition.json"
									sh "aws ecs register-task-definition --cli-input-json file://taskDefinition.json"
								}
							}
					}

						stage("Run ECS Task") {
							steps {
								script {
									sh "aws ecs run-task --cluster your-ecs-cluster --task-definition ${TASK_FAMILY} --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[${SUBNET_IDS}],securityGroups=[${SECURITY_GROUP_ID}]}'"
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
			}
		}
    }
}