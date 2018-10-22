# Dwitter

Dwitter is Twitter which was Twitter before Twitter

- View all the dweets from followed folks
- Add new dweets
- Like someone's dweet
- Comment on the dweet
- Search and follow new dweeters
- Search dweets
- Create new account (Auth)

# Getting Started

These instructions will get you a copy of the project up and running on your local machine to validate the assignment. Please See deployment for notes on how to deploy the project.

# Prerequisites

Prerequisites can be found int requirements.txt file in the project root directory.

Python 3.6
Django 2.1.2
djangorestframework 3.8.2

# Installing

## prerequisites

Below command will install project dependencies.

pip install -r requirements.txt

# Setup

## DataBase setup

By default project is configured to run on sqlite database. If you wish to test the assignment with sqlite. There is no further change required.

If you wish to change to postgresql, Please follow the below steps.

### PostgreSQL

Create DEV DataBase under user "postgres"
CREATE DATABASE dwitter_dev

Create PROD DataBase under user "postgres"
CREATE DATABASE dwitter_prod

If you wish to change user, please change in the settings module under PROJECT_ROOT/dwitter/settings/

Note: Update the respective username/password

### Running migrations

Run the below commands to create project related tables

python manage.py makemigrations
python manager.py migrate

Note: You dont need to create superuser for this project as you can create from the Dwitter application.

### Running the server as development

To run the server locally, use below command. (port=8081, default=8000)

python manage.py runserver 8081

Please change the port number as you see fit

This will run the project in dev mode and dev related settings will be imported. I recommened this to run in dev first. Later you can check run on prod. 

Dev will have additional tools.

### Running the server as production

set environment variable as below. Hope mac will have same as other unix system export.

1. export environment=prod
2. export static_file_path= PATH_TO_STATIC_FILES

You need to provide this path when you deploy django with other webservers.

# Running the tests

There are 11 test cases I have wrote for the dweets and userprofile. Use the below command to run from all apps.

1. python manage.py test

if you wish to run tests indvidually, use the below command.

1. python manage.py test dweetfeed.dweets
2. python manage.py test userprofile

You can review the test cases and let me know if you need clarification or if you want to add some other test cases to perfrom.

# Accessing the url

By default Dwitter will be running in http://localhost:8081/.

This will open the login page. As there are no users created while setting up, please do the following steps to create users.

1. Click "Register" in the login page. It will redirect you to the registration page.
2. Please provide all the details as they are mandatory.
3. Once user is registered, it will redirect you to the login page.

Please follow the above steps to create more users to test.

After creating users, you can login with same credentials.

# Posting a Dweet

After login, You will be able to Dweet. 

Note: It will not appear in the home page, as it is for feed. Please click "Dweets" in the profile sidebar to view your dweets/redweet.

# Commenting
You will able to comment on user dweets

# Search

## Dweets
To search Dweets in Dwitter, Please follow the below steps.

1. You will be seeing search in the top with drop down "select criteria".
2. Select "Dweet"
3. Enter your text to search
4. Click search to perform search

## Users
The steps are as above. But you have to select "People" as select criteria and search.

Both the results are display below to the new Dweet text box

# Followers, Following

You will be able to see your followers and following by clicking the link the profile nav bar.

You will be able to follow people by clicking "follow" next to each person.

Your home page will display the dweets of the people you follow.

# Redweet

You will be able to redweet by clicking "redweet" next to the dweet.
1. You will be able to see dweet in your profile under "Dweets"
2. You followers will be able to see them in their feed.

# Reaction
You will be able to like and dislike anyones dweet by clicking "thumbs up" and "thumbs down" button next to the dweet.

# Models
## Userprofile
Will have user details and followers. followers/following is achived by Self-ManyToMany relationship

## Dweets
Will have dweets details. Non-duplicate of redweet is achived by having ManyToMany relationship.

## Comments
Will have comments related to dweets

## Reaction
Will have likes, dislikes details to dweets

# Additional Information
Project has below additional configurations.

1. Custom logging middleware for request/response log
	i. Logs can be found in PROJECT_ROOT/logs/*

2. Redis cache is used with CACHEOPS (high level configuration. not granular level)
	i. Configuration can be found in "setting" module

3. Configured "django-debug-toolbar" to get insight of the performace.
	i. Able to apply cache is some places to reduce no. of queryset-sql calls

4. API documentation can be found in "http://localhost:8081/docs" in dev.
	i. This uses DRF inbuid documentation module