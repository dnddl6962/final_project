def imageName = "irt-pipeline"
def tagName = env.BUILD_NUMBER


pipeline {
	agent any

	environment {
		    AWS_ACCOUNT_ID = credentials("AWS_ACCOUNT_ID")
			AWS_ACCESS_KEY_ID = credentials("AWS_ACCESS_KEY_ID")
			AWS_SECRET_ACCESS_KEY = credentials("AWS_SECRET_ACCESS_KEY")
			SUBNET_IDS = credentials("SUBNET_IDS")
			SECURITY_GROUP_ID = credentials("SECURITY_GROUP_ID")
			EXECUTION_ROLE_ARN = "arn:aws:iam::${AWS_ACCOUNT_ID}:role/ecsTaskExecutionRole"
			TASK_FAMILY = "irt_pipeline"
			CLUSTER_NAME ="TestCluster"
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
                // GitHub에서 코드를 가져오면서 irt_pipeline 디렉토리로 이동하고 해당 디렉토리에서 Dockerfile을 사용하여 도커 이미지 빌드
                checkout([$class: 'GitSCM',
                          branches: [[name: 'main']],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [[$class: 'SubmoduleOption', recursiveSubmodules: false]],
                          submoduleCfg: [],
                          userRemoteConfigs: [[url: 'https://github.com/dnddl6962/final_project.git']]])

                dir('irt_pipeline') {
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
									//task 정의 
									def taskDefinition = """
									{
										"requiresCompatibilities": ["FARGATE"],
										"family": "${TASK_FAMILY}",
										"containerDefinitions": [
											{
												"name": "${imageName}",
												"image": "${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/${imageName}:${tagName}",
												"cpu": 4096,
												"memory": 16384,
												"memoryReservation": 8192,
												"essential": true,
												"environment": [
																{
																	"name": "aws_access_key_id",
																	"value": "${AWS_ACCESS_KEY_ID}"
																},
																{
																	"name": "aws_secret_access_key",
																	"value": "${AWS_SECRET_ACCESS_KEY}"
																}
															],
												"logConfiguration":
												 {
													"logDriver": "awslogs",
													"options": {
														"awslogs-create-group": "true",
														"awslogs-group": "/ecs/irt_pipeline",
														"awslogs-region": "ap-northeast-2",
														"awslogs-stream-prefix": "ecs"
														}
												}
											}
										],
										"volumes": [],
										"networkMode": "awsvpc",
										"memory": "16 GB",
										"cpu": "4 vCPU",
										"executionRoleArn": "${EXECUTION_ROLE_ARN}",
										"taskRoleArn": "${EXECUTION_ROLE_ARN}"
				
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
									sh "aws ecs run-task --cluster ${CLUSTER_NAME} --task-definition ${TASK_FAMILY} --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[${SUBNET_IDS}],securityGroups=[${SECURITY_GROUP_ID}],assignPublicIp=ENABLED}'"
								}
							}
						}

						stage('Check ECS Task Status') {
							steps {
								script {
									def taskArn = sh(script: "aws ecs list-tasks --cluster ${CLUSTER_NAME} --query 'taskArns[0]' --output text", returnStdout: true).trim()
									if (taskArn.empty) {
										error "서비스가 실행 중이 아닙니다."
									}
									
									def taskStatus = ''
									while (taskStatus != 'STOPPED') {
										taskStatus = sh(script: "aws ecs describe-tasks --cluster ${CLUSTER_NAME} --tasks ${taskArn} --query 'tasks[0].lastStatus' --output text", returnStdout: true).trim()
										if (taskStatus == 'PROVISIONING') {
											echo "서비스가 아직 프로비저닝 중입니다. 잠시 대기합니다..."
											sleep 10
										} else if (taskStatus == 'PENDING') {
											echo "서비스가 대기 중입니다."
											sleep 10
										} else if (taskStatus == 'RUNNING') {
											echo "작업이 여전히 실행 중입니다. 대기합니다..."
											sleep 10
										}
									}

									def stoppedReason = sh(script: "aws ecs describe-tasks --cluster ${CLUSTER_NAME} --tasks ${taskArn} --query 'tasks[0].stoppedReason' --output text", returnStdout: true).trim()
									if (stoppedReason.contains('Essential container in task exited')) {
										echo "Essential container in task exited: 다음 단계로 진행합니다."
									} else {
										error "작업이 중단되었습니다. 이유: ${stoppedReason}"
									}
                    
									
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