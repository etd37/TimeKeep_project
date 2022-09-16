# TimeKeep

TimeKeep is a web-application, which helps to track your working time.

## Installation

1.Clone the repository and create a virtual environment for it.

2.Then use command:
```bash
pip install -r requirements.txt
```
to install all required packages.

3.After that you need to create tables using command :
```bash
python manage.py makemigrations && python manage.py migrate
```
 4.Create super user using command:
```bash
python manage.py createsuperuser
```
 5.By the command from the root folder:
```bash
python manage.py runserver
```
you will launch application.


6. And finally, navigate to 
```bash
http://127.0.0.1:8000
or 
http://localhost:8000
```
through your browser or by clocking on the link through the terminal.

## Usage

1. To run application, first you need to Log In into admin panel using superuser account, which was created on step 4 of installation.

2. Then You need to create a default Free Plan for entire application over here:
![Screenshot from 2022-09-17 01-38-22](https://user-images.githubusercontent.com/99011743/190827417-2139b963-4e24-4270-ac64-b9d1331ec53a.png)

and define those values:

![Screenshot from 2022-09-17 01-49-02](https://user-images.githubusercontent.com/99011743/190827642-3ce17947-8b8c-4089-9895-2ce009bf4541.png)

Then you can save changes and logout.

3. Now, go back to the ```bash
http://127.0.0.1:8000
or 
http://localhost:8000
```

and you are ready to go :)

## License
[MIT](https://choosealicense.com/licenses/mit/)
