# **Testing**

## Start all services

```bash
docker-compose up -d
```
![images1](swappy-20260302_010710.png)

```bash
docker ps
```
![images1](swappy-20260302_011505.png)

# Test Flask 

```bash 
curl http://localhost:5000/api/customers?page=1&limit=5
```
![images1](swappy-20260302_011958.png)

# Ingest data 
```bash
curl -X POST http://localhost:8000/api/ingest 
```
![images1](swappy-20260302_020036.png)
# Get customers
```bash
curl http://localhost:8000/api/customers?page=1&limit=5 
```
![images1](swappy-20260302_020550.png)


