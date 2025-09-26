
# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing 

## Clone the repo

```bash
git clone https://github.com/shaianneh/flaskmvcSH.git
cd [project-directory]
```
## Install Dependencies

```bash
$ pip install -r requirements.txt
```

# Cli Commands Documentation 

## 1) Initialize / Seed - What it does: Drops & recreates tables, then seeds demo data: employers, staff, students, and two internships.

```bash
flask init
```
Seed Data (created by flask init)

Employers:

-Umbrella Corporation — password: pass

-Vault-Tec — password: pass

Staff

-Alice

-Bob 

Students

-Shania 

-Priyanka 

-Diaz 

Internships (pre-created)

-Backend Intern — owner: Umbrella Corporation — description: Flask + SQLAlchemy basics

-UX Research Intern — owner: Vault-Tec — description: Assist with studies and analysis

## 2) Create role users (manual) - Create extra Employer, Staff, or Student accounts by name + password.

Note that names must be unique, if you try to create the same person twice/when they already exist, you will receive a message saying so. 

COMMAND : flask create employer <name> <password> 
 
```bash
#Example
flask create employer "Hextech Industry" pass123
```

COMMAND : flask create staff <name> <password>

```bash
#Example
flask create staff Victor pass123
```

COMMAND : flask create student <name> <password>

```bash
#Example
flask create student Jace pass123
```
 
## 3) Employer commands: 

### A) Create an internship: 

COMMAND : flask employer create-position <employer_name> <internship_title> [description]
    
-Title must be unique.

-The internship is owned by <employer_name>.

Example:

```bash
flask employer create-position "Hextech Industry" "Hexcore Developer" "Hex-Crystal Analysis"
```

### B)Accept or reject a student:

COMMAND: flask employer decide <employer_name> <internship_title> <student_name> <ACCEPTED|REJECTED>

-Only the employer who owns <internship_title> can decide.

-Decision must be exactly ACCEPTED or REJECTED.

-If an employer attempts to Accept or Reject a student who is not yet on the shortlist, they will receive a message saying so. 

Example:

```bash
flask employer decide "Hextech Industry" "Hexcore Developer" Jace ACCEPTED
```

## 4) Staff commands

### A)Add a student to a shortlist:

COMMAND : flask staff shortlist <staff_name> <student_name> <internship_title>
    
-If the student is already on that internship’s shortlist, you’ll see a message saying so.

-New entries start with status PENDING.

Example:

```bash
flask staff shortlist Victor Jace "Hexcore Developer"
```

## 5) Student commands

### A)View own shortlist and employer decisions

COMMAND : flask student view-shortlist <student_name>
    
Example:

```bash
flask student view-shortlist Jace
```

