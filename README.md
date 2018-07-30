# manticora

Restaurant Application

## Limpar ambiente

```sh
docker stop $(docker ps -q -a)
docker rm -f $(docker ps -q -a)
docker volume prune -f
docker rmi -f $(docker images -q -a)
```

## Configuração do container do postgres
```sh
docker build -t manticora .
docker run --name="manticora_db" -v local_manticora:/var/lib/postgresql/data manticora
```
