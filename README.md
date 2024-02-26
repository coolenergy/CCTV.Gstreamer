<br/>
<p align="center">
  <a href="https://github.com/maiz27/portfolio">
    <img src="https://github.com/Maiz27/portfolio/blob/master/src/assets/imgs/logo.png?raw=true" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">CCTV</h3>
</p>

> Python Version : 3.9.0

## Setup all programs & python packages
> 
- Open terminal `Ctrl + Alt +t`
- Run Command `sudo ./env.sh`

## ENV file
> Set Configuration with .env file
```sh
# Database URL
DATABASE_URI = "postgresql://postgres:iwantbefree@localhost/db_products"

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_IP = "localhost"
DB_NAME = "db_products"
DB_PORT = "5432"

# ROOT PATH FOR VIDEO & THUMBNAILs
ROOT_PATH = "/share"

# DIR PATH FOR STOR OF RANDOM IMAGES
RAMDOM_IMAGES = "/share/random"
```
## Run Server
> python main.py
