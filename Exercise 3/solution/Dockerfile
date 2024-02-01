FROM minio/minio
WORKDIR .

CMD dnf update
CMD dnf upgrade

CMD dnf install python
CMD pip install -r requirements.txt

CMD wget https://dl.min.io/client/mc/release/linux-amd64/mc
CMD chmod +x mc

expose 9001

CMD ["minio", "server", "start", "--console-address", ":9001"]

# ENTRYPOINT [ "bin/sh" , "-c", "dnf update"]
# ENTRYPOINT [ "bin/sh" , "-c", "./mc alias set server_name http://127.0.0.1:9000/ minioadmin minioadmin"]

# CMD ./mc alias set server_name http://127.0.0.1:9000/ minioadmin minioadmin
# CMD ./mc admin user add server_name admin adminadmin
# CMD ./mc admin policy attach server_name consoleAdmin --user admin