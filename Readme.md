Test task for Huli.inc

Before run: unzip an .env file and place it in a folder, password to the archive is `potato`

In order for the emails to come with a proper address
modify the unzipped vars.env file and include proper 
HOST_IP and HOST_PORT variables (or just HOST_IP, if you require), 
and proper ADMIN_EMAIL variable.

In order to change the port the app runs on, change `docker.compose.yaml`, default port is 8000

To run: execute `docker compose up`.
