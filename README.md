# OWASP-ZAP with Drone pipeline

## Walk through of the infrastructure
The steps you should follow would be, read the `README.md` in the following order:
1. pipeline-instruction
2. gitea
3. droneCI

## Soteria's DevSecOps Pipeline
Our pipeline runs in Kubernetes.

* Code pipeline (Source code): Opens PR for feature branch -> master branch
Secret detection, static analysis and image scanning will run in the pipeline. If it passes all the tests, update and push image into the image registry. If fails, break the pipeline.
        
<img width="676" alt="code pipeline" src="https://user-images.githubusercontent.com/58884456/124769606-f1c39e80-df7c-11eb-90ce-641d6f634aa0.png">

* GitOps pipeline (Config manifest): Opens PR for the new release manifest.
<img width="1368" alt="GitOps pipeline" src="https://user-images.githubusercontent.com/58884456/124769802-1e77b600-df7d-11eb-9eac-671ea28f4df8.png">



kubelint runs towards the manifests config files.
If it passes all the tests, developer can merge the PR, otherwise the pipeline blocks the PR from merging.
        
ArgoCD is monitoring the GitOps repo. So once the PR gets merged into main branch, ArgoCD will realise the change since the Kubernetes cluster’s manifest and GitOps manifest are different.

ArgoCD will update and deploy with new GitOps Repo’s manifest. By having `argocd app wait APPNAME` step in the pipeline, it won't go to the next step until the sync is done, and once the sync is done (aka. ArgoCD deployed on Kubernetes Dev Cluster) fuzzer runs toward that live server. 
(Note that fuzzer needs (documentation, openAPI) && (Active server)  )
   
## Inside Drone CI Pipeline
```
kind: pipeline
type: docker
name: default

steps:        
- name: cd
  image: argoproj/argocd-cli
  commands:
  - argocd app wait APPNAME

- name: fuzzer
  image: owasp/zap2docker-stable
  commands:
  - Some commands to run the fuzzer towards the active target server
    -> Successful: Pipeline will send webhook to Gitea to notify the developer that the dynamic testing was successful.
    -> Failure: Breaks the pipeline
```

Our demo pipeline only covers the dev cluster, but ideally in the real world, for the production cluster we will open a new PR in order to push code from dev cluster to prod cluster Kubernetes.
        
