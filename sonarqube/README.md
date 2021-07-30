# SonarQube

To install the Helm Chart from the GitHub Repository, you can use the following commands:
```
helm dependency update
kubectl create namespace sonarqube
helm upgrade --install -f values.yaml -n sonarqube sonarqube ./
```
After pods are running:
```
export POD_NAME=$(kubectl get pods --namespace sonarqube -l "app=sonarqube,release=sonarqube" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $POD_NAME 8080:9000 -n sonarqube
```
Naviagte to http://127.0.0.1:8080/

Use the default login:

* User:admin  
* Password:admin

Change password to "password" (Just to test).

# SonarScan

Navigate to desired folder to scan.

```
wget https://raw.githubusercontent.com/9447-team-4/main/infrastructure/sonarqube/sonar-project.properties
docker run --rm -v $(pwd):/usr/src --network=host sonarsource/sonar-scanner-cli

```
Naviagte to http://127.0.0.1:8080/ to view results.

# Sonarqube on Jenkins

On Jenkins navigate to "Manage Jenkins", click on "Manage Plugins" and install "SonarQube Scanner for Jenkins".

On Jenkins navigate to "Manage Jenkins", click on "Global Tool Configuration".

* Locate "SonarQube Scanner:.  
* Click "SonarQube Scanner installations", click "Add SonarQube Scanner"  
* Under SonarQube Scanner.  
	* Specify "Name" as "sonarqube"  
	* Click "Install automatically"

On Jenkins navigate to "Manage Jenkins", click on "Configure System".

* Locate "SonarQube servers" in "Configure System".  
* Specify "Name" as "sonarqube".  
    * Specify "Server URL" as:
```
http://sonarqube-sonarqube.sonarqube.svc.cluster.local:9000
```  
* Add a "Server authentication token".  
* Kind: "secret text", secret: get from sonarqube (SonarQube->My Account->Security->Generate Tokens).  

# Create new pipeline

Under Pipeline place the following code block or use JenkinFile.
```
node {
  stage('SCM') {
    git 'https://github.com/foo.git'
  }
  stage('SonarQube analysis') {
    def scannerHome = tool 'sonarqube';
    withSonarQubeEnv('sonarqube') {
      sh "${scannerHome}/bin/sonar-scanner \
      -Dsonar.projectKey=test \
      -Dsonar.sources=."
    }
  }
  stage("Quality Gate"){
    timeout(time: 1, unit: 'HOURS') {
      def qg = waitForQualityGate()
      if (qg.status != 'OK') {
        error "Pipeline aborted due to quality gate failure: ${qg.status}"
      }
    }
  }
}
```

# Create SonarQube Webhook

On SonarQube navigate to "Administration".

On SonarQube navigate to "Configurations" and select "Webhooks".

* Create a webhook.
* Specify "URL" as:
```
http://jenkins.jenkins.svc.cluster.local:8080/sonarqube-webhook/
```  

Now you should be all setup!