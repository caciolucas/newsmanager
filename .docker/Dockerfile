# syntax=docker/dockerfile:1

##########################
# Base Stage
##########################
FROM python:3.12 AS base

# Cria o usuário "docker" e configura seu home
RUN useradd --create-home --shell /bin/bash docker && \
    mkdir -p /home/docker/workspace && \
    chown -R docker:docker /home/docker

WORKDIR /home/docker/workspace

# Instala dependências do sistema (como root)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Altera para o usuário "docker"
USER docker

# Atualiza o pip e instala pip-tools
RUN pip install --upgrade pip && pip install pip-tools

# Adiciona o diretório onde os executáveis do pip-tools (como pip-compile) foram instalados
ENV PATH="/home/docker/.local/bin:${PATH}"

##########################
# API Stage
##########################
FROM base AS api
# Copia o código da aplicação
COPY --chown=docker:docker . .
# Copia apenas o arquivo de requisitos de produção
COPY --chown=docker:docker requirements.in .
# Compila e instala as dependências de produção
RUN make requirements
# Expondo a porta da API
EXPOSE 8000
CMD ["gunicorn", "newsmanager.wsgi:application", "--bind", "0.0.0.0:8000"]

##########################
# Worker Stage
##########################
FROM base AS worker
COPY --chown=docker:docker . .
COPY --chown=docker:docker requirements.in .
RUN make requirements
CMD ["celery", "-A", "newsmanager", "worker", "--loglevel=info"]

##########################
# Scheduler Stage
##########################
FROM base AS scheduler
COPY --chown=docker:docker . .
COPY --chown=docker:docker requirements.in .
RUN make requirements
CMD ["tail", "-f", "/dev/null"]
CMD ["celery", "-A", "newsmanager", "beat", "--loglevel=info"]

##########################
# Dev Stage
##########################
FROM base AS dev
COPY --chown=docker:docker . .
# Copia os arquivos de requisitos de produção e de desenvolvimento
COPY --chown=docker:docker requirements.in .
COPY --chown=docker:docker requirements-dev.in .
# Compila e instala as dependências de produção e desenvolvimento
RUN make dev-requirements
# Mantém o container em execução para o devcontainer attachar
CMD ["tail", "-f", "/dev/null"]
