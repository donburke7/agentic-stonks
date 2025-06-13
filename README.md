# Agentic FinNews Analyst
This project aims to build an agent-assisted financial news analysis system.

## Project Setup
**_NOTE: All instructions are for macOS, other OS compatible instructions coming soon..._**

### Create .env
Create a file called _.env_ and copy the following contents into it.
Retrieve appropriate credentials from project owners.
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

### Docker Setup
#### Download Docker Desktop
Downloading and Installing Docker Desktop will include
Docker Engine, Docker Compose, Docker CLI and a GUI for easier container management.
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

#### Spin up the container
Use ```docker compose up -d``` to create the container.  
Once created, you can verify that it is running by checking 
Docker Desktop to see if container _marketrisk_postgres_ is running.

Here are some other useful Docker commands for managing the container:
- Use ```docker start marketrisk_postgres``` to start running the container.
- Use ```docker stop marketrisk_postgres``` to stop the container from running, but keep all data.
- Use ```docker compose down``` to delete the container and its data.
- Use ```docker volume ls``` and ```docker volume inspect [VOLUME_NAME]``` to inspect the volume where data is stored.
### Local Database Setup
#### Install posgreSQL@15 using Homebrew
```brew install postgresql@15```

#### Download SQL IDE 
- [DataGrip (Preferred)](https://www.jetbrains.com/datagrip/download/)
- [DBeaver](https://dbeaver.io/download/)
- [Oracle SQL Developer](https://www.oracle.com/database/sqldeveloper/technologies/download/)

For this documentation, we'll be referring to the setup process using DataGrip.

Create a new postgreSQL datasource with the following information:
- Name: ```INSERT DB NAME@localhost```
- Host: ```localhost```
- Port: ```5432```
- Authentication: ```User & Password```
- User: ```INSERT DB USERNAME```
- Password: ```INSERT DB PASSWORD```
- Database: ```INSERT DB NAME```

Test the connection and if successful, hit _OK_.

#### Without SQL IDE
Simply run 
```psql -h localhost -p 5432 -U [DB_USER] -d [DB_NAME]``` 
to connect to the database from the terminal.

