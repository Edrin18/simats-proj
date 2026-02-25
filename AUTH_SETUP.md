# Create a comprehensive setup guide
setup_guide = '''# 🔐 Authentication Setup Guide - SIMATS Hub

## 📱 PART 1: Mobile OTP (SMS)

### Option A: Test Mode (No real SMS - RECOMMENDED for testing)
By default, the app works in **test mode**. OTPs will be printed in your terminal/console.

**How to use:**
1. Enter your mobile number on the login page
2. Check your terminal/command prompt for the OTP
3. Enter that OTP to login

### Option B: Real SMS (Production)

To send actual SMS to mobile numbers, you need to set up **Fast2SMS**:

#### Step 1: Get Fast2SMS API Key
1. Go to [fast2sms.com](https://www.fast2sms.com/)
2. Create an account
3. Complete KYC verification
4. Add balance (minimum ₹10-50 for testing)
5. Go to Dashboard → API Key
6. Copy your API Key

#### Step 2: Set Environment Variable

**Windows (Command Prompt):**
```cmd
set SMS_API_KEY=your_actual_api_key_here
python app.py
```

**Windows (PowerShell):**
```powershell
$env:SMS_API_KEY="your_actual_api_key_here"
python app.py
```

**Permanent (Windows System Settings):**
1. Search "Environment Variables" in Start Menu
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `SMS_API_KEY`
6. Variable value: `your_actual_api_key_here`
7. Click OK, restart VS Code/Terminal

**Linux/Mac:**
```bash
export SMS_API_KEY=your_actual_api_key_here
python app.py
```

---

## 🔵 PART 2: Google OAuth (One-Click Login)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click "Select a project" → "New Project"
4. Project name: `SIMATS Hub`
5. Click "Create"

### Step 2: Enable Google+ API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google+ API" or "Google People API"
3. Click on it and press "Enable"

### Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" (for testing with any Gmail)
3. Click "Create"
4. Fill in:
   - App name: `SIMATS Hub`
   - User support email: your-email@gmail.com
   - Developer contact information: your-email@gmail.com
5. Click "Save and Continue"
6. On "Scopes" page, click "Add or Remove Scopes"
7. Add these scopes:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
   - `openid`
8. Click "Update" → "Save and Continue"
9. On "Test users" page, click "Add Users"
10. Add your Gmail address
11. Click "Save and Continue"

### Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Web application"
4. Name: `SIMATS Hub Web Client`
5. **Authorized redirect URIs:**
   - For local testing: `http://localhost:5000/auth/google/callback`
   - For production: `https://yourdomain.com/auth/google/callback`
6. Click "Create"
7. Copy your **Client ID** and **Client Secret**

### Step 5: Set Environment Variables

**Windows (Command Prompt):**
```cmd
set GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
set GOOGLE_CLIENT_SECRET=your-client-secret
python app.py
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
$env:GOOGLE_CLIENT_SECRET="your-client-secret"
python app.py
```

**Permanent:**
Add both `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to Windows Environment Variables (same steps as SMS_API_KEY above).

---

## 🧪 Testing Checklist

### Test Mobile OTP:
1. Go to `http://localhost:5000/login`
2. Click "Mobile Number (OTP)"
3. Enter name: `Test User`
4. Enter phone: `9876543210`
5. Check terminal for OTP (in test mode)
6. Enter OTP and verify
7. Complete profile with roll number, department, year

### Test Google OAuth:
1. Configure Google OAuth as above
2. Go to `http://localhost:5000/login`
3. Click "Continue with Google"
4. Select your Google account
5. Should login successfully!

---

## 🚀 Deployment (Render.com)

When deploying to Render:

1. Go to your Web Service dashboard
2. Click "Environment" tab
3. Add these variables:
   - `SECRET_KEY` = random-long-string-here
   - `SMS_API_KEY` = your-fast2sms-key (optional)
   - `GOOGLE_CLIENT_ID` = your-google-client-id
   - `GOOGLE_CLIENT_SECRET` = your-google-secret

4. Update Google OAuth redirect URI in Google Cloud Console to:
   `https://your-app-name.onrender.com/auth/google/callback`

---

## ❓ Troubleshooting

### SMS not sending?
- Check if you have balance in Fast2SMS
- Verify API key is correct
- Check terminal for error messages
- Use test mode to see OTP in terminal

### Google OAuth not working?
- Make sure redirect URI matches exactly (including http/https)
- Check if Google+ API is enabled
- Verify Client ID and Secret are correct
- Check if your email is added as test user

### "Authentication not configured" error?
- Environment variables are not set
- Restart your terminal/VS Code after setting variables

---

## 📞 Need Help?

- **Fast2SMS**: [Documentation](https://docs.fast2sms.com/)
- **Google OAuth**: [Google Identity Docs](https://developers.google.com/identity/protocols/oauth2)
- **Flask**: [Flask-Login Docs](https://flask-login.readthedocs.io/)

---

**Note**: For college projects, Mobile OTP is usually sufficient. Google OAuth is optional but provides better user experience! 🎓