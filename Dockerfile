# Use a imagem base do Python
FROM python:3.9

# Configuração do diretório de trabalho
WORKDIR /code/

# Atualiza e instala dependências do sistema
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* && \
    sed -i -e 's/# pt_BR ISO-8859-1/pt_BR ISO-8859-1/' -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt /code/

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto para o diretório de trabalho
COPY . .

ENTRYPOINT ["/entrypoint.sh"]