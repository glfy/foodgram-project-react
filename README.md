# <p align="center">  Foodgram </p>

<p id="description">Embark on a culinary journey with Foodgram – your ultimate online platform for sharing, discovering, and creating recipes that tantalize the taste buds. From delectable delights to must-try masterpieces, we've got your cooking inspiration covered.

Foodgram isn't just a recipe repository; it's a vibrant community of food enthusiasts. Whether you're a seasoned chef or a kitchen newbie, Foodgram invites you to explore a world of flavors, connect with fellow foodies, and showcase your culinary creations. Get ready to embark on a gastronomic adventure like no other!</p>

## 🧐 Features

Here's a taste of what Foodgram has to offer:

* 🍳 Discover a diverse collection of recipes to suit every palate.
* 🍕 Connect with other food enthusiasts, share tips, and engage in culinary conversations.
* 🍣 Curate your own recipe favorites and shopping lists for hassle-free meal planning.

## 🛠️ Installation Steps

### Installation

<p>1. Clone the repository</p>

```
git clone https://github.com/glfy/foodgram-project-react.git
cd foodgram
```

<p>2. Create and activate a .env file like in .env.example:</p>

```
Database settings
POSTGRES_USER=[database_username]
POSTGRES_PASSWORD=[database_password]
POSTGRES_DB=[database_name]
DB_PORT=[database_connection_port]
DB_HOST=[db]

Django settings
SECRET_KEY='your_secret_key'
DEBUG=True
ALLOWED_HOSTS='localhost,your_domain'
```

### Building Docker Images

<p>1. Replace username with your DockerHub username:</p>

```
cd frontend
docker build -t username/foodgram_frontend .
cd ../backend
docker build -t username/foodgram_backend .
cd ../nginx
docker build -t username/foodgram_gateway .
```

<p>2. Push images to DockerHub:</p>

```
docker push username/foodgram_frontend
docker push username/foodgram_backend
docker push username/foodgram_gateway
```

### Deploy on a Remote Server

<p>1. Connect to the remote server:</p>

```
ssh -i path_to_SSH_key_file/SSH_key_file_name username@server_ip
```

<p>2. Create a foodgram directory on the server:</p>

```
mkdir foodgram
```

<p>3. Install Docker Compose on the server:</p>

```
sudo apt update
sudo apt install curl
curl -fsSL <https://get.docker.com> -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose
```

<p>4. Copy docker-compose.production.yml and .env files to the foodgram/ directory:</p>

```
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
```

<p>5. Run Docker Compose in daemon mode:</p>

```
sudo docker-compose -f docker-compose.production.yml up -d
```

<p>6. Create Superuser and fill database if needed:</p>

```
# Get into the backend container
docker exec -it foodgram_backend_container_name /bin/bash
# Access the Django Shell
python manage.py shell
python3 manage.py createsuperuser 
# The system will ask for credentials, after which a superuser will be created.

# Also you can create superuser by running:
python manage.py create_admin
# credentials would be: 
password = a
username = admin
email = a@a.ru

# To fll the database with sample data, run:
python manage.py create_tags
python manage.py import_csv

# This will create sample ingridients and tags to populate the database.
```

<p>7. Open the Nginx config:</p>

```
sudo nano /etc/nginx/sites-enabled/default
```

<p>8. Adjust location settings:</p>

```
location / {
proxy_set_header Host $http_host;
proxy_pass <http://127.0.0.1:8888>;
}
```

<p>9. Test Nginx config:</p>

```
sudo nginx -t
```

<p>10. Reload Nginx:</p>

```
sudo service nginx reload
```

### CI/CD Configuration

<p>1. The workflow file is available here:</p>

```
foodgram/.github/workflows/main.yml
```

<p>2. Customize for your server by adding GitHub Actions secrets:</p>

```
DOCKER_USERNAME # DockerHub username
DOCKER_PASSWORD # DockerHub password
HOST # Server's IP address
USER # Username
SSH_KEY # Private SSH key (cat ~/.ssh/id_rsa)
SSH_PASSPHRASE # SSH key passphrase
```

## 🌐 Explore the App

🔗 Link to the deployed application: [Foodgram](https://foodgramkotafilippa.hopto.org)

🔗 There is also an API. To view the available paths, follow the link: [API](https://foodgramkotafilippa.hopto.org/api/).

🔗 And the api documentation is here: [Docs](https://foodgramkotafilippa.hopto.org/api/docs/).

🔗 ip address = 84.252.141.139



##

## 💻 Built with

Experience the magic of these technologies:

* Python - backend powerhouse
* Django Rest Framework - Python toolkit for Web APIs
* JavaScript - frontend dynamism
* React - crafting splendid user interfaces
* Gunicorn - Python WSGI HTTP Server
* Nginx - your trusty HTTP and reverse proxy server

## 👩‍💻 Team

* backend: [Daria Gelfman](https://github.com/glfy)
* frontend: a creative cuisine creator
* devops [Daria Gelfman](https://github.com/glfy)
* reviewer [Roman Reznikov](https://github.com/ReznikovRoman)

##

<p align="center">
  Made with ❤️ by Foodgram Team
</p>
