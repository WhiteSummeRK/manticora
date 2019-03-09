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
docker build -t ezfood .
docker run --name="ezfood_db" -p 5432:5432 -v local_manticora:/var/lib/postgresql/data ezfood
```

## Executar as migrações
```sh
python migrations.py db init
python migrations.py db migrate
python migrations.py db upgrade
```
