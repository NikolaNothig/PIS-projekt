## Employee managment
This project is employee managment application for adding, editing, deleting and filtering employees.
Whole list and details of employees will be shown inside application. The table consists of the name, surname, age, email of employees as well as of their paycheck and position in the company.
![image](https://github.com/NikolaNothig/PIS-projekt/assets/115481213/d41129f3-4e81-405b-8944-d1f662c41aee)
![image](https://github.com/NikolaNothig/PIS-projekt/assets/115481213/eef5fb7d-fc76-4ef4-9467-0472a826f36d)


## Features
-Add a new employee
-Edit employee
-Delete employee
-Filter employee by paycheck and by position

## Running the Backend
Application is run on docker

#### Creating a docker image
```sh
cd PIS Projekt
docker build -t employeemanagment -f ./Dockerfile .
```

#### Running the docker image
```sh
docker run -p 5000:5000 employeemanagment
```

## Preview the frontend
Open and navigate to the templates folder and run *index.html* with browser.
