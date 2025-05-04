#  Farming Management System (FMS)

The **Farming Management System (FMS)** is a full-stack web platform designed to empower farmers by enabling them to sell their produce directly to consumers online. This system reduces dependency on intermediaries, enhances profit margins, and makes the agricultural supply chain more transparent and efficient.

Developed as part of **DSCI-D 532: Applied Database Technologies**, this project implements modern web technologies, relational databases, and secure authentication practices to serve farmers, buyers, and system administrators.

---

##  Project Overview

-  **Farmers** can register, list products, set prices, and track sales.
-  **Consumers** can browse listings, send inquiries, and negotiate deals.
-  **Admins** can manage user accounts, listings, and system operations.

The platform supports full CRUD operations, session-based authentication, secure password storage, and audit logging through MySQL triggers.

---

##  Key Features

-  Secure registration & login (hashed passwords)
-  Product listing with pricing, quantity & description
-  Role-based access (Farmer, Buyer, Admin)
-  Direct interaction between buyers and farmers
-  MySQL Triggers to auto-log database changes
-  Responsive UI with Bootstrap

---

##  Tech Stack

| Layer         | Technology Used                                |
|---------------|-------------------------------------------------|
| **Frontend**  | HTML5, CSS3, JavaScript, Bootstrap 5            |
| **Backend**   | Python (Flask), SQLAlchemy                      |
| **Database**  | MySQL (via XAMPP & phpMyAdmin)                  |
| **Server**    | XAMPP (Apache + MySQL)                          |
| **Tools**     | Git, GitHub, VSCode                             |

---

## ⚙️ Setup Instructions (Full Installation Guide)

###  Step 1: Install XAMPP

1. Download XAMPP for your OS from:  
    [https://www.apachefriends.org/index.html](https://www.apachefriends.org/index.html)

2. Run the installer and select these components:
   - **Apache**
   - **MySQL**
   - **phpMyAdmin**

3. Launch the **XAMPP Control Panel** and start:
   -  **Apache**
   -  **MySQL**

4. Open **phpMyAdmin** in your browser:  

---

###  Step 2: Set Up MySQL Database

1. Create a database named `fms`.

2. Import the provided SQL file (`database.sql` or `fms_schema.sql`) from this repo into phpMyAdmin:
- Click on your database
- Go to the **Import** tab
- Upload and run the `.sql` file

---

###  Step 3: Clone the Project Repository

```bash
git clone https://github.com/Harsha85018/Farming_Management_System_FMS.git
cd Farming_Management_System_FMS
