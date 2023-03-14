APPLICATION FORM

The project implements a system for registering user requests.

The system consists of the following elements:
- frontend, pages: login, registration, application form, application’s registration history;
- backend, files: app.py, helpers.py;
- database: application.db.


Description of the "frontend" element:

The user's request acceptance page, contains elements:
- Last Name field (text type)
- First Name field (text type)
- Patronymic field (text type)
- Phone field (phone type, to simplify the numbers)
- Address field (large text type)
- the "Send" button (initializes sending data to the backend)

Implementation: html, sending to the backend.


Description of the "backend" element:

A service that implements the functionality of receiving data from the frontend, forming an object and writing to the database.
Implementation: python (flask), sqlite3

Description of the " database" element:

SQL database contains 2 tables:

-	Apps:

|Column	|Field	      |Type      |
|:------|:------------|---------:|
| 0     | user_id     | INTEGER	 |
| 1	    | app	        | TEXT	 |
| 2	    | datetime    | DATETIME |
| 3	    | complete    | BOOLEAN	 |
| 4		  | name	      | TEXT	 |
| 5		  | lastname    | TEXT	 |
| 6		  | patronymic  | TEXT	 |
| 7	    | phonenumber | NUMERIC	 |

- Users:

| Column	| Field	    | Type	 |
|---------|-----------|-------:|
| 0	      | id		    | INTEGER|
| 1	      | username	| TEXT   |
| 2		    | hash	    | TEXT	 |


