# SEA-Salon, 2024/07/02

This is my submission for COMPFEST 16 Software Engineering Academy. My biggest Thank you for reading this and I hope this simple readme files can help you try my submission. Feel free to contact through email me if there is something you wanted to ask for. 

- email = fairuz.akbar.azaria@mail.ugm.ac.id

## Technologies

The main technology behind this project is **Python**. I'm using Python **Flask** to built my project. For the database, I'm using **CockroachDB's** PostgreSQL. I then deploy this project using **Docker** on my personal **Alibaba Linux server**.

## System Architectures

This project is made by using **MVC architectures**. It display data through **Views**, process data through **controllers**, and stores data in a database **models**. I have also allowed the architectures to be **modularized**, therefore each modules can be easily taken out or added. This creates an environment where each modules becomes almost independent from one another. I achieved this by using **Flask Blueprints** and separated my applications into 2 main modules, the **Main App module**, and the **API module**.

### a. Main App Module
This is my main module and it function as the one that manage all child modules within the application. It also contains the main views that are supposed to be seen by the clients. Unfortunately due to current university exams, I am unable to finish the views part. But I have designed its user interface. If you are interested, you can view it here on my [Figma file](https://www.figma.com/design/dJiI7fn8yLXTjFIz1tShDj/Salon?node-id=28-3745).

### b. API Module

This is where any requests are being process, For more detailed endpoints data and its example, I have simplified it in my Postman API Collection in this Repository.

***Notes**: All request parameters are in raw JSON format*

***Notes**: Some request required Admin privileges*

## Installation and Usage

There is no need to install anything since the application is already deployed. To try and access the application API, you need to import the postman collection json files into Postman. All the available endpoints are there to access. But before trying around the endpoints, it is recommended to perform authorization with following steps:

1. Access Endpoint Login, perform login using credentials given
2. After that we need to update the current token and refresh token variable in Postman
2. If token becomes invalid, I might suggest to refresh token or simply login again

To access the API base URL, you can use this link:
```bash
8.215.10.89:5000/api
```

Below are some user data you can use for authentication purposes:
```bash
{
    "user_email": "thomas.n@compfest.id",
    "user_password": "Admin123"
}
```

```bash
{
    "user_email": "majid.martin@mail.id",
    "user_password": "Cstmr123"
}
```

### Application Installation on Local Machine using Docker

If you want to install my application in your local machine, I highly advise using docker since I have packaged all the required version and environments to make it easy to deploy. If you are interested, you can also view this project's docker images in [my docker hub repository](https://hub.docker.com/repository/docker/fairuzazaria/sea-salon/general). Below are some of the steps you can follow to do install my application on your local machines using docker:

1. Login to Docker Hub (*a password prompt will appear*)
```bash
docker login -u {docker_hub_username}
```
2. Pull docker image
```bash
docker pull fairuzazaria/sea-salon:v1.1
```
3. Run docker image on port 5000
```bash
docker run -d -p 5000:5000 -e PYTHONUNBUFFERED=1 fairuzazaria/sea-salon:v1.1
```
4. Make sure container is running
```bash
docker ps
```
5. You are ready to access the API endpoints 
```bash
8.215.10.89:5000/api
```

***Notes**: make sure to have docker installed before installation*

***Notes**: don't forget to adjust base_url variable in the postman collection as well*