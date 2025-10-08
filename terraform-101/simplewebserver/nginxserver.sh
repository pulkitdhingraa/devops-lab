#!/bin/bash

sudo yum update -y

sudo amazon-linux-extras enable nginx1
sudo yum install -y nginx

cat <<EOF > /usr/share/nginx/html/index.html
    <html>
        <head>
            <title>Welcome</title>
        </head>
        <body>
            <h1>Hello from Nginx</h1>
        </body>
    </html>
EOF

sudo systemctl start nginx
sudo systemctl enable nginx