# Gitea

Gitea, gitea Gitea?

## Installation

### kubernetes
First install helm by:

```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Then, navigate to the helm-chart folder and run (only has to be done once):
```
helm dependency update 
```
Finally, navigate to the root gitea folder and run:
```
kubectl create namespace gitea ; kubectl create quota test --hard=count/persistentvolumeclaims=4 --namespace=gitea ; helm install gitea-charts helm-chart/ --values helm-chart/values.yaml --namespace gitea
```
This will add 3 pods to your "gitea" namespace.

## Usage
To open a UI to the gitea server run:
```
kubectl -n gitea port-forward gitea-charts-0 3000:3000
```
The ui is accesible from any browser at localhost:3000  
The default admin account is:
```
  admin:
    username: gitea_admin
    password: r8sA8CPHD9!bt6d
    email: "gitea@local.domain"

```

# Server Side Hooks (GGshield)

## Installation

Make sure python is installed in the gitea/default namespace

ie.
```
apk add --no-cache python3 py3-pip
```
OR
```
sudo apt-get update
sudo apt-get install python3
```

Then, install ggshield:

```python
pip install ggshield
```

### Server Side Template

The following instructions will make all new repos contain the GG pre-receive hooks.

If you haven't made any repos yet, navigate to the gitea folder and run (copy into
whatever namespace gitea is in): 
```
kubectl cp hooks/ <NAMESPACE>/gitea-charts-0:usr/share/git-core/templates
```
Then, get a shell to the gitea namespace, navigate to the template folder and 
give execute, write and read permissions to all template hooks.
```
cd usr/share/git-core/templates/hooks
chmod -R +rwx *
```

### Individual Repos

If there are existing repos and you want to add the pre-receive hook there,
navigate the the gitea UI and:

- Navigate to the repo on an admin account
- Settings -> git hooks tab
- Copy the following:

```bash
#!/bin/bash

export GITGUARDIAN_API_KEY=12c19DfDb724381acbbf0dDb58C36A13fA514efD9cddFff9FC9Ff2201BDE0dAd6f5CA57

# Commit sha with all zeros
zero_commit="0000000000000000000000000000000000000000"

while read -r oldrev newrev refname; do
    # Check if a zero sha
    if [ "${oldrev}" = "${zero_commit}" ]; then
        # List everything reachable from newrev but not any heads
        span="$(git for-each-ref --format='%(refname)' 'refs/heads/*' | sed 's/^/\^/') ${newrev}"
    else
        span="${oldrev}...${newrev}"
    fi

    ggshield scan commit-range "${span}" && continue

    echo "ERROR: Your push was rejected because it contained a security incident"
    echo "ERROR: Please contact your Git administrator if this was a false positive."
    exit 1
done
```

- Edit the pre-receive hook from the gitea UI, paste the above in.

# Dumpster Diver

Shelved (for now)
