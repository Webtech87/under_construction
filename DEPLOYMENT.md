# Deployment on Render

## Environment Setup

- **Python**: 3.13.2
- **Django**: 5.1.5
- **Hosting**: Render.com
- Static files served via **WhiteNoise**

## Installing Dependencies

1. **Create & Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

2. **Install gunicorn**
```bash
pip install gunicorn
```

3. **Create build.sh**
In your root directory, create a `build.sh` file with the following content:
```bash
#!/bin/bash 

set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
```

4. **Install and configure Whitenoise**
Install whitenoise:
```bash
pip install whitenoise
```
To configure **Whitenoise**, go to `settings.py` and add `STATIC_ROOT` towards the bottom of the file:
```bash
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
Make sure you’re using the static template tag to refer to your static files, rather than writing the URL directly. For example:
```bash
{% load static %}
<img src="{% static "images/hi.jpg" %}" alt="Hi!">

<!-- DON'T WRITE THIS -->
<img src="/static/images/hi.jpg" alt="Hi!">
```
Now you need to enable **Whitenoise** at your `settings.py`:
```bash
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```
For detailed information, visit Whitenoise's documentation.

5. **Update requirements.txt**
```bash
pip freeze > requirements.txt
```

6. **No Database needed**  
For this project, no database is needed, so you can delete any folder, file or piece of code automatically created by **Django** related to databases.

## Deploying on Render

1. **New Project**  
After creating an account on Render and logging in, click on **New** (top-right corner) and choose **Web Service**.

2. **Logging in to you GitHub Account**  
You will need to give Render permission to access your repositories. After giving permission, it can take a few minutes to Render to connect to your GitHub account.

3. **Choosing project on GitHub**  
You can choose the repository you want to deploy. After choosing, click on **Connect**.

4. **Deploying a Web Service**
- In the New Web Service page, give a name to your Web Service (or leave as it is).
- Choose the repository's branch you want to deploy.
- Choose the Region which best matches your location (if you do not find your region, choose the closest one).
- Edit the **Build Command** to:
```bash
sh build.sh
```
- Edit the **Start Command** to:
```bash
$ gunicorn name-of-folder-containing-your-settings.py.wsgi:application
```

5. **Environment Variables**

- You need to manually set your Environment Variables on Render. On the Environment Variables field, you can click on *Add from .env*. It will popup a little window and you can copy and paste all your secret variables from your secret file.
- Your service key will need to be transformed into a `base64` string, as Render does not support directly `.json` files in Environment Variables.
    - In your command line, run the command:
    ```bash
    base64 -i your-service-key.json > encoded_file.txt
    ```
    This will create a enconded_file.txt file, with the `base64` string, in the directory you run the command.
- In your `views.py` you will need to convert your `base64` string into `.json` again.
```bash
CLIENT_SECRET_BASE64 = os.getenv('name-of-your-env-variable-on-render')

# Decode the base64 string and write the content to a temporary file
decoded_credentials = base64.b64decode(CLIENT_SECRET_BASE64)
secret_file_path = '/tmp/your-secret-folder/your-service-key.json'

# Ensure the directory exists
os.makedirs(os.path.dirname(secret_file_path), exist_ok=True)

with open(secret_file_path, 'wb') as f:
    f.write(decoded_credentials)
```

6. **Finishing Deployment Process**  
After setting up your environment variables, select a plan and click on **Deploy Web Service**.  
There are 2 different situations about the website's domain:
- If you choose the free plan, when deployment starts, **Render** will generate a random URL for your project.
- But if you choose a paid plan, you can use a custom domain.  
Either way, you need to update `ALLOWED_HOSTS` and add `CSRF_TRUSTED_ORIGINS` in your `settings.py`:
- Free plan:
```bash
ALLOWED_HOSTS = ['your-random-render-url.onrender.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['your-random-render-url.onrender.com']
```
- Paid plan:
```bash
ALLOWED_HOSTS = ['your-custom-domain.com','your-random-render-url.onrender.com', 'localhost', '127.0.0.1'] #You can choose leaving or not Render's generated URL
CSRF_TRUSTED_ORIGINS = ['your-custom-domain.com','your-random-render-url.onrender.com']
```
After that, push the changes to your repository on GitHub. Render will automatically deploy the changes.