# Quick APK Installation Guide

## Get Your APK (Choose One Method)

### Method 1: Download from GitHub Actions (Recommended)

1. **Go to GitHub Actions:**
   - Visit: `https://github.com/blooop/scratch_env/actions`
   - Or click **Actions** tab in your repository

2. **Find the Build:**
   - Click on the latest **"Android CI - Build APK"** workflow run
   - Look for a green checkmark ✅

3. **Download APK:**
   - Scroll to bottom → **Artifacts** section
   - Click **year-calendar-debug-apk** to download
   - A ZIP file will download

4. **Extract:**
   - Unzip the downloaded file
   - You'll find `app-debug.apk` inside

### Method 2: Build Locally (If you have Android Studio)

```bash
cd YearCalendar
./gradlew assembleDebug
# APK will be at: app/build/outputs/apk/debug/app-debug.apk
```

## Install on Your Android Phone

### Option A: Direct Install (Easiest)

1. **Transfer APK to your phone:**
   - Email it to yourself and download on phone
   - Use Google Drive / Dropbox
   - Connect phone via USB and copy to Downloads folder
   - Use ADB (if you know how)

2. **Enable Unknown Sources:**
   - Open **Settings** on your phone
   - Go to **Security** or **Privacy**
   - Find **Install unknown apps** or **Unknown sources**
   - Enable for your **File Manager** or **Chrome** (wherever you downloaded the APK)

3. **Install:**
   - Open **File Manager** or **Downloads** app
   - Find `app-debug.apk`
   - Tap it
   - Tap **Install**
   - Wait for installation
   - Tap **Open**

### Option B: Using ADB (For Developers)

```bash
# Connect phone via USB with USB debugging enabled
adb install app-debug.apk
```

## First Launch Setup

1. **Open the app** (Year Calendar)

2. **Tap "Sign in with Google"**

3. **Select your Google account**

4. **Grant permissions:**
   - Allow access to Google Calendar
   - Read calendar events

5. **Wait for calendar to load**

6. **Start using!**
   - Pinch to zoom in/out
   - Drag to pan
   - Tap year at top to change years

## ⚠️ IMPORTANT: OAuth Setup Required

For the app to work, you need to configure the SHA-1 fingerprint in Google Cloud Console:

### Get SHA-1 from Debug Keystore

On your computer, run:
```bash
keytool -list -v -keystore ~/.android/debug.keystore \
  -alias androiddebugkey -storepass android -keypass android
```

Copy the **SHA-1** fingerprint (looks like: `A1:B2:C3:D4:...`)

### Add to Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your Google Cloud project
3. Navigate to **APIs & Services** → **Credentials**
4. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
5. Choose **Android**
6. Fill in:
   - **Package name:** `com.yearcalendar.app`
   - **SHA-1 certificate fingerprint:** Paste the SHA-1 from above
7. Click **Create**

Now the app will work!

## Troubleshooting

### "App not installed" error

**Solutions:**
- Uninstall any previous version first
- Make sure you enabled "Install from unknown sources"
- Check you have Android 8.0 or higher
- Try redownloading the APK

### "Sign in failed" error

**Solutions:**
- Make sure you added SHA-1 to Google Cloud Console (see above)
- Check internet connection
- Try signing out and in again
- Verify Calendar API is enabled in Google Cloud Console

### No events showing

**Solutions:**
- Pull down to refresh
- Try a different year (tap year at top)
- Check you have events in Google Calendar for that year
- Sign out and sign in again

### App crashes on startup

**Solutions:**
- Clear app data: Settings → Apps → Year Calendar → Clear Data
- Reinstall the app
- Check Android version is 8.0+

## Minimum Requirements

- **Android Version:** 8.0 (Oreo) or higher
- **Internet:** Required for first sign-in and loading events
- **Google Account:** With Google Calendar access
- **Storage:** ~50 MB

## App Permissions

The app requests:
- **Internet access** - To connect to Google Calendar
- **Network state** - To check connectivity

That's it! No camera, location, or other invasive permissions.

## Uninstalling

To remove the app:
1. Go to **Settings** → **Apps**
2. Find **Year Calendar**
3. Tap **Uninstall**

This will remove all app data including stored tokens.

## Getting Updates

When a new version is released:
1. Download the new APK from GitHub Actions
2. Install over the existing app (no need to uninstall)
3. Your settings and login will be preserved

## Security Note

This is a **debug APK** signed with Android's default debug certificate. It's safe for personal use but not suitable for distribution.

For production use:
- Generate a release keystore
- Sign with your own certificate
- Upload to Google Play Store (recommended)

## Need Help?

Check the full documentation:
- `README.md` - Overview and features
- `SETUP_GUIDE.md` - Development setup
- `CI_SETUP.md` - CI/CD configuration
- `SECURITY.md` - Security policies

Enjoy your Year Calendar! 📅
