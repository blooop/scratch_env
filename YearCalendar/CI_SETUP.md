# CI/CD Setup for Year Calendar

This project uses GitHub Actions to automatically build APKs on every push.

## GitHub Secrets Configuration

To enable automatic APK builds, you need to add your OAuth credentials as GitHub repository secrets.

### Step 1: Navigate to Repository Settings

1. Go to your GitHub repository: `https://github.com/blooop/scratch_env`
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Step 2: Add Required Secrets

Add these three secrets:

#### Secret 1: GOOGLE_CLIENT_ID
- Name: `GOOGLE_CLIENT_ID`
- Value: Your Google OAuth Client ID (format: `xxx-xxx.apps.googleusercontent.com`)

#### Secret 2: GOOGLE_CLIENT_SECRET
- Name: `GOOGLE_CLIENT_SECRET`
- Value: Your Google OAuth Client Secret (format: `GOCSPX-xxxxx`)

#### Secret 3: GOOGLE_PROJECT_ID
- Name: `GOOGLE_PROJECT_ID`
- Value: Your Google Cloud Project ID

**Note:** Use the OAuth credentials that were provided to you separately.

### Step 3: Verify Secrets

After adding all three secrets, you should see:
- ✅ GOOGLE_CLIENT_ID
- ✅ GOOGLE_CLIENT_SECRET
- ✅ GOOGLE_PROJECT_ID

## How CI/CD Works

### Automatic Builds

The workflow automatically triggers on:
- **Push** to branch `claude/android-calendar-year-view-Ckk5P`
- **Pull requests** to `main` branch
- **Manual trigger** via GitHub Actions UI

### Build Process

1. Checks out code
2. Sets up Java 17
3. Injects OAuth credentials from secrets into `local.properties`
4. Builds debug APK
5. Builds release APK (unsigned)
6. Uploads APKs as artifacts

### Build Artifacts

After a successful build, you can download the APKs:

1. Go to the **Actions** tab in your repository
2. Click on the latest workflow run
3. Scroll down to **Artifacts** section
4. Download:
   - `year-calendar-debug-apk` - Ready to install on any device
   - `year-calendar-release-apk` - Optimized but unsigned

## Downloading Your APK

### Method 1: From GitHub Actions UI

1. Navigate to: `https://github.com/blooop/scratch_env/actions`
2. Click on the most recent **"Android CI - Build APK"** workflow run
3. Scroll to bottom → **Artifacts** section
4. Click **year-calendar-debug-apk** to download
5. Extract the ZIP file
6. Transfer `app-debug.apk` to your Android device

### Method 2: Using GitHub CLI

```bash
# List recent workflow runs
gh run list --workflow=android-build.yml

# Download artifacts from latest run
gh run download --name year-calendar-debug-apk
```

## Installing APK on Android Device

### Enable Installation from Unknown Sources

1. On your Android device, go to **Settings**
2. Navigate to **Security** (or **Apps & notifications** → **Special app access**)
3. Enable **Install unknown apps** for your file manager or browser

### Install the APK

#### Method A: Direct Download
1. Open the downloaded ZIP on your Android device
2. Extract `app-debug.apk`
3. Tap the APK file
4. Tap **Install**
5. Tap **Open** when installation completes

#### Method B: ADB Install
```bash
# Connect device via USB with USB debugging enabled
adb install app-debug.apk
```

#### Method C: Wireless Transfer
1. Upload APK to Google Drive or similar
2. Download on Android device
3. Open and install

## Manual Build (Alternative)

If you need to build locally:

```bash
cd YearCalendar

# Create local.properties with credentials
echo "google.client.id=YOUR_CLIENT_ID" > local.properties
echo "google.client.secret=YOUR_SECRET" >> local.properties
echo "google.project.id=YOUR_PROJECT_ID" >> local.properties

# Build debug APK
./gradlew assembleDebug

# APK location
ls -lh app/build/outputs/apk/debug/app-debug.apk
```

## Workflow File Location

The CI/CD configuration is located at:
```
.github/workflows/android-build.yml
```

## Troubleshooting

### Build Fails with "Secrets not found"

**Solution:** Ensure all three secrets are added to GitHub repository settings.

### Build Fails with Gradle Errors

**Solution:** Check the workflow logs in the Actions tab for detailed error messages.

### APK Not Generated

**Solution:**
1. Check if the workflow ran successfully (green checkmark)
2. Verify the YearCalendar directory has changes
3. Look at workflow logs for errors

### APK Won't Install on Device

**Symptoms:** "App not installed" or "Package conflicts"

**Solutions:**
- Uninstall any previous version first
- Enable installation from unknown sources
- Check Android version is 8.0 (API 26) or higher
- Verify APK file isn't corrupted (re-download if needed)

### SHA-1 Fingerprint Issues

The debug APK is signed with Android's default debug keystore. The SHA-1 is:
```
Keystore: ~/.android/debug.keystore
Alias: androiddebugkey
Password: android
```

To get the SHA-1:
```bash
keytool -list -v -keystore ~/.android/debug.keystore \
  -alias androiddebugkey -storepass android -keypass android
```

**Important:** For the APK to work with Google OAuth, you need to add this SHA-1 to your Google Cloud Console OAuth credentials.

## Production Release

For a production-signed APK:

1. Generate a release keystore:
   ```bash
   keytool -genkey -v -keystore release.keystore \
     -alias year-calendar -keyalg RSA -keysize 2048 -validity 10000
   ```

2. Add keystore secrets to GitHub:
   - `RELEASE_KEYSTORE` (base64 encoded keystore file)
   - `RELEASE_KEYSTORE_PASSWORD`
   - `RELEASE_KEY_ALIAS`
   - `RELEASE_KEY_PASSWORD`

3. Update workflow to sign release builds

4. Register release SHA-1 in Google Cloud Console

## Security Notes

✅ **Secure:**
- Secrets are encrypted in GitHub
- Not exposed in logs
- Only accessible during workflow runs
- Automatically injected into build

⚠️ **Best Practices:**
- Rotate secrets periodically
- Use different credentials for production
- Never commit secrets to repository
- Review workflow runs for unauthorized access

## Build Status

Check the current build status:

[![Android CI](https://github.com/blooop/scratch_env/actions/workflows/android-build.yml/badge.svg)](https://github.com/blooop/scratch_env/actions/workflows/android-build.yml)

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Android CI Best Practices](https://developer.android.com/studio/build)
- [APK Installation Guide](https://www.androidauthority.com/how-to-install-apks-31494/)

## Support

If you encounter issues:
1. Check workflow logs in Actions tab
2. Review error messages
3. Verify secrets are configured correctly
4. Ensure device meets minimum requirements (Android 8.0+)
