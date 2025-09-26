#!/bin/bash

# Derruba todos os containers em execução
docker stop $(docker ps -aq)

# Remove todos os containers
docker rm -f $(docker ps -aq)

# Remove todas as imagens
docker rmi -f $(docker images -aq)

# Remove todos os volumes
docker volume rm -f $(docker volume ls -q)

# Remove todas as redes não utilizadas
docker network prune -f

# Remove cache de build
docker builder prune -af
