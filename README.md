# Dr. Paula – Under Construction Page

This is an **under construction** page for Dr. Paula, a psychologist, preceding the launch of the full website. The page provides users with the ability to request information by filling out a contact form. 

## Features

- **Call-to-Action (CTA) Button**  
  - Opens a modal popup with a form.

- **Contact Form**  
  - Users provide personal details, select a subject of interest, and write a message.  
  - Links to **Terms & Conditions** and **Privacy Policy** are included.  
  - Form submission:  
    - Sends data to Dr. Paula’s email.  
    - Updates a **Google Sheets file** via the **Google API**.  
    - If the file doesn't exist, it is **created automatically** with predefined headers.

- **Cookie Management**  
  - Users can **accept or reject cookies**.  
  - A **Cookies Policy link** is available.

- **Social Media & Contact**  
  - Facebook & Instagram icons redirect to Dr. Paula’s official pages.  
  - An email icon allows direct contact.

## Technologies Used

- **Backend:** Django  
- **Frontend:** HTML, CSS, Bootstrap  
- **Google API Services:** Google Sheets API, Google Drive API  
- **Deployment:** Render  

## Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/Webtech87/under_construction.git
cd path/to/your/local/repo
```

2. **Create & Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables in a secret file inside a secret folder**
```bash
SECRET_KEY = 'your-secret-key'
EMAIL_SENDER = 'your-email-sender' 
EMAIL_SENDER_PASSWORD = 'your-email-sender-app-password'
RECAPTCHA_PUBLIC_KEY = 'your-recaptcha-public-key'
RECAPTCHA_PRIVATE_KEY = 'your-recaptcha-private-key'
```
You will need a service key from Google Cloud Console to run Google API. After downloading it, store it in a `.env` file inside your secret folder:
Example:
```ini
CLIENT_SECRET = your-secret-folder/your-service-key.json
```

5. **Run the server**
```bash
python manage.py runserver
```