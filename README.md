
# MinIO + JFrog + Kubernetes Demo (Real-Time Style)

This project shows a **realistic end-to-end workflow**:

1. Deploy MinIO (S3-compatible storage) into Kubernetes.
2. Deploy JFrog Artifactory (Docker registry) into Kubernetes (via Helm).
3. Build a simple Python API that uses **boto3** to talk to MinIO.
4. Build a Docker image, push it to **JFrog Docker registry**.
5. Deploy that image into Kubernetes.

> ⚠️ This project is designed for **learning**. Do **not** use these exact configs in production
> without adding security, backup, and monitoring.

---

## 0. Prerequisites

You should have:

- Windows 10/11 with **PowerShell**
- A running Kubernetes cluster and `kubectl` configured (Minikube, Kind, Rancher, etc.)
- **Docker Desktop** installed and running
- Internet access

You will install:

- `helm` (Kubernetes package manager)
- Python and required libraries (inside the container)

---

## 1. Install Helm (on Windows)

Open **PowerShell** as Administrator and run:

```powershell
winget install Helm.Helm
```

After install, verify:

```powershell
helm version
```

You should NOT see the error `helm: The term 'helm' is not recognized...`.

If `winget` is not available, you can download Helm manually from the official website.

---

## 2. Create Namespace

We will keep everything inside a dedicated namespace: `demo-minio-jfrog`.

Run:

```powershell
cd <path-to-unzipped-folder>

kubectl apply -f k8s/namespace.yaml
```

---

## 3. Deploy MinIO to Kubernetes

We deploy a **single-node MinIO** with:

- One Deployment
- One Service
- One Secret (access key / secret key)

Apply:

```powershell
kubectl apply -f k8s/minio-secret.yaml
kubectl apply -f k8s/minio-deployment.yaml
kubectl apply -f k8s/minio-service.yaml
```

To check:

```powershell
kubectl get pods -n demo-minio-jfrog
kubectl get svc -n demo-minio-jfrog
```

To access MinIO UI (port-forward):

```powershell
kubectl port-forward -n demo-minio-jfrog svc/minio 9000:9000 9001:9001
```

Then open:

- MinIO Console (UI): http://localhost:9001
- S3 API endpoint: http://localhost:9000

Use the credentials from `k8s/minio-secret.yaml` (by default: `minioadmin` / `minioadmin123`).

In the MinIO Console, create a **bucket** named `demo-bucket`.

---

## 4. Deploy JFrog Artifactory (Docker Registry)

We use the official **JFrog Artifactory Helm chart**.

### 4.1 Add Helm repo

```powershell
helm repo add jfrog https://charts.jfrog.io
helm repo update
```

### 4.2 Install Artifactory (basic)

> ⚠️ This is a **very basic** config. For real use, read JFrog docs carefully.

```powershell
helm install artifactory   jfrog/artifactory   --namespace demo-minio-jfrog   --create-namespace
```

Wait until pods are ready:

```powershell
kubectl get pods -n demo-minio-jfrog
```

### 4.3 Access JFrog UI

You can use port-forward:

```powershell
kubectl port-forward -n demo-minio-jfrog svc/artifactory 8082:8082
```

Then open:

- http://localhost:8082

Complete the setup wizard, create an **admin user**, then create a **Docker registry** (e.g., `docker-local`).

Assume your Docker registry URL is:

- `localhost:8082/docker-local`

Write it down; you will use it in Docker commands.

---

## 5. Build the Python App Image

The sample app is under `app/`.

### 5.1 Inspect the app

- `app/main.py` – FastAPI app using boto3 and MinIO
- `app/requirements.txt` – dependencies
- `app/Dockerfile` – how to build the image

### 5.2 Build Docker image

From project root:

```powershell
cd app

# Replace YOUR_DOCKER_REGISTRY with your JFrog Docker registry (e.g., localhost:8082/docker-local)
$env:DOCKER_REGISTRY = "localhost:8082/docker-local"

docker build -t $env:DOCKER_REGISTRY/minio-demo-app:1.0.0 .
```

---

## 6. Login to JFrog Docker Registry & Push Image

Login (replace username & password with your JFrog credentials):

```powershell
docker login $env:DOCKER_REGISTRY
```

Push image:

```powershell
docker push $env:DOCKER_REGISTRY/minio-demo-app:1.0.0
```

If push succeeds, you’ll see the image inside JFrog UI under the `docker-local` repository.

---

## 7. Deploy the App to Kubernetes (Using JFrog Image)

Now edit `k8s/app-deployment.yaml` and make sure the `image:` line points to:

```yaml
image: localhost:8082/docker-local/minio-demo-app:1.0.0
```

Apply:

```powershell
kubectl apply -f k8s/app-configmap.yaml
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
```

Check:

```powershell
kubectl get pods -n demo-minio-jfrog
kubectl get svc -n demo-minio-jfrog
```

Port-forward the app:

```powershell
kubectl port-forward -n demo-minio-jfrog svc/minio-demo-app 8000:80
```

Open the docs:

- http://localhost:8000/docs

---

## 8. Test the Endpoints

### 8.1 Upload a file

Use `/upload` endpoint, send a file (e.g., via Swagger UI `/docs`).

The app will:

- Receive the file
- Put it into the MinIO `demo-bucket`
- Return the object key

### 8.2 List files

Call `/list` endpoint; it lists all objects in `demo-bucket`.

---

## 9. Clean Up

To uninstall everything:

```powershell
helm uninstall artifactory -n demo-minio-jfrog

kubectl delete -f k8s/app-service.yaml
kubectl delete -f k8s/app-deployment.yaml
kubectl delete -f k8s/app-configmap.yaml

kubectl delete -f k8s/minio-service.yaml
kubectl delete -f k8s/minio-deployment.yaml
kubectl delete -f k8s/minio-secret.yaml

kubectl delete -f k8s/namespace.yaml
```

---

## 10. Next Steps (Real-Time Enhancements)

To make this even more “real-time project style”:

- Add **Ingress** with a domain (e.g., using Nginx Ingress Controller)
- Add **TLS certificates** (Let’s Encrypt via cert-manager)
- Store JFrog & MinIO passwords in **Kubernetes Secrets**
- Use **Terraform** to automate Kubernetes & Helm installs
- Add **GitHub Actions / GitLab CI** to build & push images automatically
# minio-jfrog-k8s-demo-implemented
