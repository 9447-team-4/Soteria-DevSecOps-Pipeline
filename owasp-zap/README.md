# OWASP-ZAP
Perform an api scan on a REST API defined web application through OpenAPI 3.0.
# zapGenAPI
Generates an OpenAPI 3.0 json file with input server url specification

Requirements
```
pip install pyyaml
```
Usage
```
python3 zapGenAPI.py [-h] -f  -u

optional arguments:
  -h, --help    show this help message and exit
  -f , --file   openAPI json or yaml file
  -u , --url    url of server
  
  
Example
python3 zapGenAPI.py -f ~/openapi/openAPI.yaml -u http://127.0.0.1:8080
```
Output
```
zap_openapi.json
```
# Zed Attack Proxy (ZAP)
Pull docker image
```
docker pull owasp/zap2docker-stable
```
Navigate to generated api file's folder

Run the docker mounting current directory
```
docker run --network=host -v "$(pwd)/:/zap/wrk/" owasp/zap2docker-stable python3 zap-api-scan.py -t zap_openapi.json -f openapi -r report.html
```
Output
```
report.html
```
