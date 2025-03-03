**README - Client Usage Guide**

## 1. Using the Client
This client is a command-line tool designed to interact with the Information Visualization API. Ensure that you have Python installed on your system.

### **Installation**
Before running the client, install the required dependencies:
```bash
pip install requests
```

### **Running the Client**
To start the client, navigate to the directory containing `commandline.py` and run:
```bash
python commandline.py
```

### **Command List & Usage**
| Command | Description | Example |
|---------|-------------|----------|
| `list` | View all available modules | `list` |
| `login <url>` | Log in to the system | `login https://sc22ag2.pythonanywhere.com/login/` |
| `logout` | Log out of the system | `logout` |
| `register` | Register a new user | `register` |
| `view` | View professor ratings | `view` |
| `average <prof_id> <module_code>` | Get a professor's average rating for a module | `average TT1 PG1` |
| `rate <prof_id> <module_code> <year> <semester> <rating>` | Submit a professor rating | `rate TT1 PG1 2017 2 4` |

## 2. **PythonAnywhere Domain**
The client interacts with the service hosted at:
**https://sc22ag2.pythonanywhere.com/**

## 3. **Admin Login Credentials**
To access the Django Admin Panel, go to:
**https://sc22ag2.pythonanywhere.com/admin/**

⚠️ **Important:** The admin password should not be stored in plaintext in this file. Please request login credentials securely from the administrator.

## 4. **Additional Information**
- Ensure you **log in** before submitting a professor rating.
- If you encounter issues, verify that your internet connection is active and the API service is running.
- Contact support if you experience authentication or access issues.

---
End of `readme.txt`


