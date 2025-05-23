# Restaurant-Management
Repository for the restaurant management project work (software engineering).
 Instructions on how to run it on your PC:
 PLEASE SCROLL TO THE BOTTOM OF THIS README FILE FOR USERS AND PASSWORDS

---

### **1️⃣ Clone the Repository**
First, clone the repository to their local machine:
```bash
git clone <repository_url>
```
Replace `<repository_url>` with the URL of your team’s repository (e.g., GitHub or GitLab link).

Navigate into the project directory:
```bash
cd <repository_folder>
```

---

### **2️⃣ Set Up a Virtual Environment**
It's best to work in a virtual environment to avoid conflicts with global Python packages.

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

---

### **3️⃣ Install Project Dependencies**
Ensure you have Python and `pip` installed. Then, install the required Python packages by running:
```bash
pip install -r requirements.txt
```

> **Note**: Make sure your `requirements.txt` file is up-to-date and contains all the packages your project needs (e.g., Django, Pillow).

---

### **4️⃣ Set Up the Database**
Run Django’s migrations to set up the database schema:
```bash
python manage.py migrate
```

---

### **5️⃣ Collect Static Files**
If your project uses static files (e.g., CSS, JavaScript, images), collect them into the `staticfiles` directory:
```bash
python manage.py collectstatic
```
> you can press `yes` (`y`) if prompted about overwriting files.

---

### **6️⃣ Start the Development Server**
To run the project locally, you can start Django’s built-in development server:
```bash
python manage.py runserver
```

This will start the server at `http://127.0.0.1:8000/`. you can visit this URL in their browser to see the application in action.

---

### **7️⃣ Configure Environment Variables**
If the project uses sensitive information (e.g., API keys, database credentials), ensure these variables are provided via a `.env` file or their operating system’s environment. For example:
- Create a `.env` file in the project root:
  ```plaintext
  SECRET_KEY=your_secret_key
  DEBUG=True
  DATABASE_URL=your_database_url
  ```
- Make sure Django reads these variables using a library like `python-decouple` or `django-environ`.

---

### **8️⃣ Optional: Load Sample Data**
If the repository includes fixtures or sample data, you can load it into the database:
```bash
python manage.py loaddata <fixture_file.json>
```

---

### **Common Issues**
- **Dependencies Missing**: Ensure Python is updated and all dependencies are installed (`pip install -r requirements.txt`).
- **Database Not Configured**: Verify the database settings in `settings.py` or via environment variables.
- **Static Files Missing**: Run `collectstatic` as shown above.

---

### **Key Requirements**
Make sure to list these in your `README.md` for the repo:
1. **Python Version** (e.g., Python 3.10+ recommended).
2. **Dependencies**: `requirements.txt`.
3. Instructions for environment setup and running the server.

   Role : Username: password 
The first three are for the employee portal

Manager: Manager: e44mtyaKfQU3REU  

Waiter: EdwardJay : v8zwisKRwkqFsyM

Chef : chef_pete : MZQ48Q2MzN8cfai

To log in the admin site visit this url while server is running : http://127.0.0.1:8000/admin/
the username is admin and the password is admin.

This is where you can also add menu items and their pictures .You can also populate all the database tables in the admin site
If these user accounts are not available you can create your own in the admin site by going to users and creating one then go to the userprofile table to assign a role to the user you would have just created.  You should now be able to login with those user credentials in the employee portal of the site.


