## 一、安裝 ollama

```yaml
oc apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ollama-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama
        command: ["ollama"]
        args: ["serve"]
        ports:
        - containerPort: 11434
        volumeMounts:
        - name: ollama-storage
          mountPath: /.ollama
        resources:
          requests:
            memory: "4Gi"
          limits:
            memory: "6Gi"
      volumes:
      - name: ollama-storage
        persistentVolumeClaim:
          claimName: ollama-data
---
apiVersion: v1
kind: Service
metadata:
  name: ollama
spec:
  selector:
    app: ollama
  ports:
    - protocol: TCP
      port: 80
      targetPort: 11434
  type: ClusterIP
EOF
```

## 二、模型

```bash
oc exec -it <ollama-pod-name> -- bash
ollama run llama3.2:1b
```

## 三、測試

```bash
curl -X POST "http://ollama-swhsu0917-dev.apps.rm2.thpm.p1.openshiftapps.com/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Hello Ollama, can you tell me a joke?"
  }'
```
