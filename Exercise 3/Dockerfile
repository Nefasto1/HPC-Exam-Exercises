FROM minio/minio:latest
WORKDIR .
COPY requirements.txt ./
COPY docker_command.sh ./
RUN apt update
RUN apt upgrade -y
RUN apt install python3-pip -y
RUN apt install wget -y
RUN pip install -r requirements.txt
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc
EXPOSE 9000
EXPOSE 9001
RUN chmod +x mc
RUN docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"
RUN ./mc alias set admin http://127.0.0.1:9000/ minioadmin minioadmin
RUN ./mc user add server_name admin admin
RUN ./mc admin policy attach server_name consoleAdmin --user admin