# Digital Database with Privacy and Authentication Features

## 📌 Project Overview

This project is a **Privacy-Aware Digital Database System**, developed as a semester project for the **Information Security course** at **FAST-NUCES, Karachi**. It is designed to allow **viewing**, **insertion**, **updating**, and **deletion** of data records in a secure and consent-driven environment.

The system incorporates **authentication**, **role-based access control**, **audit logging**, and **user privacy features**, ensuring both ethical and secure handling of user and admin data.

---

## 👥 Group Members

- **Jahanzeb Khairi (22K-4746)**
- **Murtaza Rizvi (22K-4754)**
- **M. Yahya Khan (22K-4690)**

---

## 🔐 Key Features

- **Three user roles**:
  - **Admin**: Can register new admins with an admin key, manage the database.
  - **Special User**: Requires a **one-time password (OTP)** for registration, with limited insert/view access.
  - **Normal User**: Has view-only access to admin database, requires valid admin name and key.

- **Authentication System**:
  - Uses **hashed passwords** for login authentication.
  - Admin keys are hashed and validated for secure access to databases.

- **Consent & Audit Logging**:
  - Every database action is preceded by **user consent**.
  - All actions are logged in:
    - `consent.txt` (user consent logs)
    - `audit.txt` (action and timestamp logs)

- **Data File Structure**:
  - Admins automatically get files generated upon registration:
    - `{admin}_product.txt`
    - `{admin}_quantity.txt`
    - `{admin}_buy.txt`
    - `{admin}_sell.txt`
    - `{admin}_time.txt`
  - These store the digital database details.

- **Role-Based Access Control**:
  - Admins manage full database functionality.
  - Special users and users must **specify an existing admin name and key** to access that admin’s database.

---

## 📁 File System Structure

```plaintext
.
├── code.py                  # Main Python implementation
├── audit.txt                # Logs of all database actions with  timestamps
├── consent.txt              # Logs of user consents for each action
├── admin.txt                # Registered admin usernames
├── special.txt              # Registered special user usernames
├── user.txt                 # Registered normal user usernames
├── password1.txt            # Hashed passwords for admins
├── password2.txt            # Hashed passwords for special users
├── password3.txt            # Hashed passwords for normal users
├── admin_key.txt            # Hashed admin keys for access validation
├── {admin}_product.txt      # Product names (admin-specific)
├── {admin}_quantity.txt     # Product quantities (admin-specific)
├── {admin}_buy.txt          # Buy prices (admin-specific)
├── {admin}_sell.txt         # Sell prices (admin-specific)
├── {admin}_time.txt         # Timestamps of updates (admin-specific)
