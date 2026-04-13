# 1. Usamos uma imagem oficial do Python estável e leve
FROM python:3.12-slim

# 2. Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Define a pasta de trabalho dentro do container
WORKDIR /app

# 4. Instala dependências do sistema necessárias para o conector do Postgres
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o restante do código do projeto para dentro do container
COPY . /app/

# 7. Expõe a porta que o Django usa
EXPOSE 8000