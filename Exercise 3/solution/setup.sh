# Run the server
sudo docker run -d -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"

# Install the requirements
pip install -r requirements.txt

# Download the mc software if not already done
if ! [ -f "$PWD/mc" ];
then
    wget https://dl.min.io/client/mc/release/linux-amd64/mc
    chmod +x mc
fi

# Set the admin access
./mc alias set server_name http://127.0.0.1:9000/ minioadmin minioadmin
./mc admin user add server_name admin adminadmin
./mc admin policy attach server_name consoleAdmin --user admin

# Console info
clear
echo -e "Storage server is up, you can access it using the url: \n\t\e]8;;127.0.0.1:9001\a127.0.0.1:9001\e]8;;\a or \e]8;;172.17.0.2:9001\a172.17.0.2:9001\e]8;;\a"
