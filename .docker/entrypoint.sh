#!/bin/sh
set -e

# Executa as migrações
python manage.py migrate

# Executa o comando passado como argumento
exec "$@"
