import os
from dotenv import load_dotenv
import datetime

load_dotenv()

current_datetime = datetime.datetime.utcnow().isoformat() + 'Z'

# Calculate end datetime (30 days ahead)
end_datetime = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat() + 'Z'

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")

# Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

# For multi-tenant app
AUTHORITY = os.getenv("AUTHORITY")
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

# Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.
REDIRECT_PATH = os.getenv("REDIRECT_PATH")

# This resource requires no admin consent
# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={current_datetime}&enddatetime={end_datetime}"

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = [os.getenv("SCOPE")]

# Specifies the token cache should be stored in server-side session
SESSION_TYPE = os.getenv("SESSION_TYPE")
