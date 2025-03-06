from django.shortcuts import render
from .forms import ContactRequestForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

# Imports for Google Drive and Sheets APIs
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import os
import base64

# Create your views here.

# Google Sheets logic

CLIENT_SECRET_BASE64 = os.getenv('CLIENT_SECRET_BASE64')

# Decode the base64 string and write the content to a temporary file
decoded_credentials = base64.b64decode(CLIENT_SECRET_BASE64)
secret_file_path = '/tmp/secret_files/service_key.json'

# Ensure the directory exists
os.makedirs(os.path.dirname(secret_file_path), exist_ok=True)

with open(secret_file_path, 'wb') as f:
    f.write(decoded_credentials)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_SENDER_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD") # Google service account file

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Get credentials
def get_credentials():
    credentials = service_account.Credentials.from_service_account_file(secret_file_path, scopes=SCOPES)

    return credentials

def search_spreadsheet_by_name(service, spreadsheet_name="pedido_informacao"):
    # Search for a sheet by name in Google Drive.
    query = f"name = '{spreadsheet_name}' and mimeType = 'application/vnd.google-apps.spreadsheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    spreadsheets = results.get('files', [])
    
    if spreadsheets:
        return spreadsheets[0]['id']  # Return the first sheet's ID found
    else:
        return None  # No sheet found
    
def share_sheet_with_email(sheet_id, email=EMAIL_SENDER):
    # Share the sheet with a Google account
    credentials = get_credentials()
    drive_service = build('drive', 'v3', credentials=credentials)

    permission = {
        'type': 'user',
        'role': 'writer',  # Use 'writer' for edit access, 'reader' for view access
        'emailAddress': email
    }

    # Apply the permission (share the sheet)
    drive_service.permissions().create(
        fileId=sheet_id,
        body=permission,
        sendNotificationEmail=False  # Change to True if you want an email notification
    ).execute()

    '''
    Print for troubleshooting
    print(f'Sheet shared with {email}')
    '''

# Create a new sheet if it doesn't exist, or return the existing sheet's ID.
def create_or_get_sheet(sheet_name='Sheet1'):
    credentials = get_credentials()

    # First, use the Drive API to check for an existing sheet
    drive_service = build('drive', 'v3', credentials=credentials)
    sheet_id = search_spreadsheet_by_name(drive_service, 'pedido_informacao')
    
    if not sheet_id:
        # If no sheet exists, create a new one using the Sheets API
        sheets_service = build('sheets', 'v4', credentials=credentials)
        spreadsheet = {
            'properties': {'title': 'pedido_informacao'}
        }
        sheet = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        sheet_id = sheet['spreadsheetId']

        # Define the headers to insert into the first row
        headers = ["Nome", "Email", "Assunto", "Mensagem"]

        # Prepare the request body to update the first row with headers
        body = {'values': [headers]}

        # Update the first row with headers
        range_ = f'{sheet_name}!A1:D1'
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_,
            valueInputOption='RAW',  # Use 'RAW' if you just want the raw data inserted, 'USER_ENTERED' for Google Sheets functions
            body=body
        ).execute()

        share_sheet_with_email(sheet_id)

         # Wait for the sheet to be fully created and populated
        '''
        Print for troubleshooting
        print(f"Headers inserted into sheet: {sheet_name}")
        '''

    else:
        '''
        Print for troubleshooting
        print(f"Sheet '{sheet_name}' already exists with ID: {sheet_id}")
        '''
        share_sheet_with_email(sheet_id)

    return sheet_id

def add_data_to_sheet(sheet_id, data, sheet_name='Sheet1'):
    # Append data to the given Google Sheet.
    credentials = get_credentials()
    service = build('sheets', 'v4', credentials=credentials)
    
    # Prepare data to be added
    body = {'values': [data]}

    range_ = f'{sheet_name}'

    # Append data to the first sheet in the document
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_,  # Adjust this range if needed
        valueInputOption='RAW',  # Ensure rows are added, not overwritten
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

def site_under_construction(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        context = {
            'form': form,
            'success': 'Mensagem enviada com sucesso.'
        }
        if form.is_valid():
            cd = form.cleaned_data
            full_name = cd['full_name']
            email = cd['email']
            subject = cd['subject']
            message = cd['message']

            data = [full_name, email, subject, message]
            # GOOGLE SHEETS
            try:
                # Create or retrieve the sheet and append data
                sheet_id = create_or_get_sheet()
                add_data_to_sheet(sheet_id, data)
            except Exception as e:
                print(f"An error occurred with Google Sheets: {e}")


            email_subject = f'Novo Formulário Preenchido'

            email_body = render_to_string('emails/contact_email.html', {
                'full_name': full_name,
                'email': email,
                'subject': subject,
                'message': message
            })  
            
            logger = logging.getLogger(__name__)
            
            try:
                email_msg = EmailMultiAlternatives(
                    subject=email_subject,
                    body=email_body,
                    from_email=EMAIL_SENDER,
                    to=[EMAIL_SENDER],
                    reply_to=[email]
                )

                email_msg.attach_alternative(email_body, "text/html")
                email_msg.send(fail_silently=False)
            
                return render(request, "test.html", context)

            # Raise error if email not sent because fail_silently=False
            except Exception as e:
                logger.error(f"Email sending failed: {e}")
                return render(request, "test.html", context)

    else:
        form = ContactRequestForm()
        context = {
            'form': form,
            'submit': 'Enviar Mensagem'
        }
    return render(request, 'test.html', context)
