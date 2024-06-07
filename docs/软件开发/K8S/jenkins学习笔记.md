# 启动jenkins docker
docker run \
  -v /usr/bin/docker:/usr/bin/docker \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /home/ubuntu/myjenkins/jenkins_home/:/var/jenkins_home \
  -u root \
  -d --name jenkins \
  -p 8120:8080 \
  jenkins/jenkins:jdk11

 # 查看token命令
cat /var/jenkins_home/secrets/initialAdminPassword

# 启动测试docker, 挂载allure报告目录
docker run \
  -v /home/ubuntu/myjenkins/jenkins_home/beifan/:/app/.allure_results/ \
  --shm-size 2G ccr.ccs.tencentyun.com/beifan/ui_framework:v1
