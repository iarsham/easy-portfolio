# Portfolio-Backend

### Introduction
Portfolio-Backend is an open source
 service where you can add data related to personal information, professional career history, personal projects, blog links and ...
### Installation Guide
* Clone this repository [here](https://github.com/Trapeziums/Portfolio-Backend.git).
* The master branch is the most stable branch at any given time, ensure you're working from it.
* Update the necessary variables according to the .env file.
* Install docker and docker-compose depending on your os. [link](https://docs.docker.com/desktop/)
### Usage
* Run the following commands
```sh
- docker network create Portfolio-Backend
- docker volume create db_data
- docker-compose up --build
```
* Note Now the project is ready at 127.0.0.1:80
* BaseUrl = https://domain.com/api/v1
<br /><br />
### API Endpoints (User)
| HTTP Verbs | Endpoints | Payload | api-key |
| --- | --- | --- | ---|
| POST | /register/ | username , email , password1 , password2 | No
| POST | /login/ | username , password or email , password | No
| POST | /login/google/ | access_token or code | No
| POST | /login/github/ | access_token or code | No
| POST | /logout/ | _ | Yes
| POST | /password_reset/ | email | No
| POST | /resend_verification_email/ | email | No
| POST | /password/change/ | old_password , new_password1 , new_password2 |Yes
| POST | /password_reset_confirm/{uid}/{token}/ | new_password1 , new_password2 , uid , token | No
| POST | /confirm-email{key}/ | key | No
| GET | /user/ | _ | Yes
| PUT | /user/ | username , email | Yes
| DELETE | /user/ | _ | Yes
| GET | /user/key/ | _ | Yes

<br /><br />

### API Endpoints (Portfolio)
| HTTP Verbs | Endpoints | Payload | api-key |
| --- | --- | --- | ---|
| GET | /aboutme/ | _ | Yes
| PUT | /aboutme/ | first_name , last_name , location , job_title , summery ,  phone_number , resume , social_accounts , file  | Yes
| DELETE | /aboutme/profile/{id}/ | _ | Yes
| GET | /education/ | _ | Yes
| PUT | /education/ | institute , field_study , degree ,  grade , description , start_time , finish_time  | Yes
| GET | /skill/ | _ | Yes
| POST | /skill/ | name , file | Yes
| PUT | /skill/ | name , file | Yes
| DELETE | /skill/{id}/ | _ | Yes
| DELETE | /skill/certificate/{id}/ | _ | Yes
| GET | /language/ | _ | Yes
| POST | /language/ | name , proficiency , file | Yes
| PUT | /language/ | name , proficiency , file | Yes
| DELETE | /language/{id}/ | _ | Yes
| DELETE | /language/certificate/{id}/ | _ | Yes
| GET | /achievement/ | _ | Yes
| POST | /achievement/ | title , description , file | Yes
| PUT | /achievement/ | title , description , file | Yes
| DELETE | /achievement/{id}/ | _ | Yes
| DELETE | /achievement/certificate/{id}/ | _ | Yes
| POST | /contactme/ | name , email , subject , message | Yes
| GET | /proficiency/ | _ | NO
| GET | /employment/ | _ | NO

<br /><br />

### API Endpoints (Experience)
| HTTP Verbs | Endpoints | Payload | api-key |
| --- | --- | --- | ---|
| GET | /experience/ | _ | Yes
| POST | /experience/ | role , employment_type , company_name , company_website_link , location , description , start_date , end_date , still_working | Yes
| PUT | /experience/{id}/ | role , employment_type , company_name , company_website_link , location , description , start_date , end_date , still_working | Yes
| DELETE | /experience/{id}/ | _ | Yes
| GET | /project/{slug}/ | _ | Yes
| POST | /project/{slug}/ | name , link , description , stacks, file | Yes
| PUT | /project/{slug}/{id}/ | name , link , description , stacks, file | Yes
| DELETE | /project/{slug}/{id}/ | _ | Yes
| DELETE | /project/asset/{slug}/{id}/ | _ | Yes
| GET | /reference/ | _ | Yes
| POST | /reference/ | full_name , email , phone_number , linkedin , recommendation , image  | Yes
| PUT | /reference/{id}/ | full_name , email , phone_number , linkedin , recommendation , image | Yes
| DELETE | /reference/{id}/ | _ | Yes
| GET | /blog/ | _ | Yes
| POST | /blog/ | title , description , link , writen_date , image | Yes
| PUT | /blog/{id}/ |  title , description , link , writen_date , image | Yes
| DELETE | /blog/{id}/ | _ | Yes
| GET | /personal_project/{slug}/ | _ | Yes
| POST | /personal_project/{slug}/ | name , link , description , stacks, file | Yes
| PUT | /personal_project/{slug}/{id}/ | name , link , description , stacks, file | Yes
| DELETE | /personal_project/{slug}/{id}/ | _ | Yes
| DELETE | /personal_project/asset/{slug}/{id}/ | _ | Yes

<br /><br />

### Technologies Used
* [Python](https://nodejs.org/) is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming.
* [Django](https://www.expresjs.org/) is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
* [Djangorestframework](https://www.mongodb.com/)  (DRF) is a powerful and flexible toolkit for building Web APIs.
* [Docker](https://mongoosejs.com/) is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.
* [Nginx](https://mongoosejs.com/) pronounced like “engine-ex”, is an open-source web server that, since its initial success as a web server, is now also used as a reverse proxy, HTTP cache, and load balancer.
* [Postgresql](https://mongoosejs.com/) is an advanced, enterprise-class, and open-source relational database system. PostgreSQL supports both SQL (relational) and JSON (non-relational) querying.
* [Git](https://mongoosejs.com/) is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

* [Celery](https://mongoosejs.com/) is a task queue implementation for Python web applications used to asynchronously execute work outside the HTTP request-response cycle.
* [Redis](https://mongoosejs.com/) is an open source (BSD licensed), in-memory data structure store, used as a database, cache, and message broker. Redis provides data structures …
### License
This project is available for use under the MIT License.
