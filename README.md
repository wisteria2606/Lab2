Поднимаем стенд в Docker
```
wisteria@HOME-PC:~/Lab2$ docker compose up -d --build
WARN[0000] /home/wisteria/Lab2/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
[+] Building 5.1s (14/14) FINISHED
 => [internal] load local bake definitions                                                                         0.0s
 => => reading from stdin 473B                                                                                     0.0s
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 462B                                                                               0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                0.1s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim                                                          0.1s
 => => resolve docker.io/library/python:3.11-slim                                                                  0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 1.46kB                                                                                0.0s
 => CACHED [builder 2/4] WORKDIR /app                                                                              0.0s
 => CACHED [stage-1 3/5] RUN useradd -m appuser && chown -R appuser /app                                           0.0s
 => CACHED [builder 3/4] COPY requirements.txt .                                                                   0.0s
 => CACHED [builder 4/4] RUN pip install --user --no-cache-dir -r requirements.txt                                 0.0s
 => CACHED [stage-1 4/5] COPY --from=builder /root/.local /home/appuser/.local                                     0.0s
 => [stage-1 5/5] COPY app/ .                                                                                      0.1s
 => exporting to image                                                                                             4.3s
 => => exporting layers                                                                                            0.1s
 => => exporting manifest sha256:7ade3030d27dddcedac5a1e00ec38c0be5620b1c82caa3e966346387752ecba6                  0.0s
 => => exporting config sha256:ca6cd1de1616a3fe919661f6bcd5801ab39a968aebb83324ee1cdb721a7b7aa8                    0.0s
 => => exporting attestation manifest sha256:6b71000f604933fc17596dce35adb9edb3dc6f4183349159f682c7c5de3a1df1      0.0s
 => => naming to docker.io/library/lab2-api:latest                                                                 0.0s
 => => unpacking to docker.io/library/lab2-api:latest                                                              4.0s
 => resolving provenance for metadata file                                                                         0.0s
[+] Running 8/8
 ✔ lab2-api                   Built                                                                                0.0s
 ✔ Network lab2_public        Created                                                                              0.1s
 ✔ Network lab2_backend       Created                                                                              0.1s
 ✔ Container lab2-adminer-1   Started                                                                              1.3s
 ✔ Container lab2-redis-1     Started                                                                              1.2s
 ✔ Container lab2-traefik-1   Started                                                                              1.3s
 ✔ Container lab2-postgres-1  Healthy                                                                              6.2s
 ✔ Container lab2-api-1       Started                                                                              6.3s
```
Проверка
```
wisteria@HOME-PC:~/Lab2$ curl -s http://api.localhost/healthz
{"status":"ok"}wisteria@HOME-PC:~/Lab2$ curl -s http://api.localhost/cache
{"cache":"ok"}wisteria@HOME-PC:~/Lab2$ curl -s http://api.localhost/db
{"db":1}wisteria@HOME-PC:~/Lab2$
```
Состояние
```
wisteria@HOME-PC:~/Lab2$ docker compose ps
NAME              IMAGE                COMMAND                  SERVICE    CREATED         STATUS                   PORTS
lab2-adminer-1    adminer              "entrypoint.sh docke…"   adminer    5 минут назад   Up 5 минут             8080/tcp
lab2-api-1        lab2-api             "uvicorn main:app --…"   api        5 минут назад   Up 5 минут
lab2-postgres-1   postgres:16-alpine   "docker-entrypoint.s…"   postgres   5 минут назад   Up 5 минут (healthy)
lab2-redis-1      redis:7-alpine       "docker-entrypoint.s…"   redis      5 минут назад   Up 5 минут
lab2-traefik-1    traefik:v3.1         "/entrypoint.sh --pr…"   traefik    5 минут назад   Up 5 минут             0.0.0.0:80->80/tcp, [::]:80->80/tcp
```
Логи
```
wisteria@HOME-PC:~/Lab2$ docker compose logs -f api
api-1  | INFO:     Started server process 
api-1  | INFO:     Waiting for application startup.
api-1  | INFO:     Application startup complete.
api-1  | INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
api-1  | INFO:     172.19.0.2:38658 - "GET /healthz HTTP/1.1" 200 OK
api-1  | INFO:     172.19.0.2:41068 - "GET /cache HTTP/1.1" 200 OK
api-1  | INFO:     172.19.0.2:50770 - "GET /db HTTP/1.1" 200 OK
```
