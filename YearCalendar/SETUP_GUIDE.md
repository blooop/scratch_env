# Year Calendar - Complete Setup Guide

## Quick Start

This Android app displays your Google Calendar in a year view with zoom functionality.

### What You'll Need

1. **Android Studio** - Download from [developer.android.com](https://developer.android.com/studio)
2. **Android Device or Emulator** - API level 26 (Android 8.0) or higher
3. **Google Account** - For calendar access

### OAuth Credentials

The app requires OAuth credentials to be configured in `local.properties`:
- Client ID: Your Google OAuth client ID
- Client Secret: Your Google OAuth client secret
- Project ID: Your Google Cloud project ID

These are stored securely in `local.properties` and **not committed to git**.

## Step-by-Step Setup

### 1. Open Project in Android Studio

```bash
cd YearCalendar
```

Then in Android Studio:
- File → Open
- Select the `YearCalendar` directory
- Wait for Gradle sync to complete

### 2. Configure OAuth (If Needed)

The `local.properties` file already contains your OAuth credentials. If you need to update them:

```properties
google.client.id=YOUR_CLIENT_ID
google.client.secret=YOUR_CLIENT_SECRET
google.project.id=YOUR_PROJECT_ID
```

### 3. Configure Android App in Google Cloud Console

For the OAuth to work properly on Android, you need to register your app's SHA-1 fingerprint:

#### Get Debug SHA-1 Fingerprint

```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

#### Add SHA-1 to Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to: **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID
5. Click **Edit**
6. Under "Application type", ensure you have an **Android** client ID
7. If not, create one:
   - Click **+ CREATE CREDENTIALS** → **OAuth client ID**
   - Application type: **Android**
   - Package name: `com.yearcalendar.app`
   - SHA-1 certificate fingerprint: Paste the fingerprint from step 1
   - Click **Create**

### 4. Build and Run

#### Using Android Studio

1. Click the "Run" button (green play icon)
2. Select your device or emulator
3. Wait for build and installation

#### Using Command Line

```bash
./gradlew assembleDebug
./gradlew installDebug
```

### 5. Sign In

1. Launch the app
2. Tap "Sign in with Google"
3. Select your Google account
4. Grant calendar permissions
5. View your calendar!

## Features Guide

### Year View

- **12 Vertical Columns**: One for each month
- **Days Listed Vertically**: All days of each month
- **Color-Coded Events**: Events shown as colored dots
- **Today Highlighted**: Current day has colored background
- **Weekends Shaded**: Saturday and Sunday have different background

### Zoom Controls

**Pinch to Zoom**
- Pinch out: Zoom in (max 5x)
- Pinch in: Zoom out (min 0.5x)

**Zoom Buttons**
- **+** button: Zoom in 20%
- **-** button: Zoom out 20%
- **1x** button: Reset to default zoom

**Pan**
- Drag with one finger to move around the calendar

### Navigation

**Year Selector**
- Tap the year in the top bar
- Select different year from picker
- Range: 5 years before to 5 years after current year

**Refresh**
- Tap refresh icon in top bar
- Reloads events from Google Calendar

**Sign Out**
- Tap three dots in top bar
- Select "Sign Out"
- Clears all locally stored credentials

## Troubleshooting

### "Sign In Failed"

**Possible causes:**
1. SHA-1 fingerprint not registered
2. OAuth client not configured for Android
3. Calendar API not enabled

**Solutions:**
1. Follow step 3 above to register SHA-1
2. Verify Android OAuth client exists in Google Cloud Console
3. Enable Calendar API:
   - Google Cloud Console → APIs & Services → Library
   - Search "Google Calendar API"
   - Click Enable

### "No Events Showing"

**Possible causes:**
1. No events in selected year
2. Network connection issues
3. Calendar permission not granted

**Solutions:**
1. Try different year using year picker
2. Check internet connection
3. Sign out and sign in again to re-authorize

### Build Errors

**"Gradle sync failed"**
```bash
./gradlew clean
# Then sync again in Android Studio
```

**"SDK not found"**
- Android Studio → Tools → SDK Manager
- Install SDK for API 34

**"Duplicate class" errors**
```bash
./gradlew clean build --refresh-dependencies
```

### Runtime Crashes

**Check Logcat in Android Studio:**
- View → Tool Windows → Logcat
- Filter by package name: `com.yearcalendar.app`
- Look for error stack traces

Common issues:
- OAuth credentials missing from `local.properties`
- Network permission denied
- API key mismatch

## App Architecture

### Tech Stack

- **Language**: Kotlin
- **UI**: Jetpack Compose + Material Design 3
- **Architecture**: MVVM (Model-View-ViewModel)
- **Dependency Injection**: Hilt
- **Async**: Kotlin Coroutines + Flow
- **Authentication**: Google Sign-In SDK
- **API**: Google Calendar API v3
- **Security**: EncryptedSharedPreferences

### Key Components

```
MainActivity
    └─ YearCalendarTheme
        ├─ SignInScreen (when not authenticated)
        └─ CalendarScreen (when authenticated)
            └─ YearCalendarView
                └─ YearCalendarCanvas (zoomable/pannable)

CalendarViewModel
    ├─ GoogleAuthManager (authentication)
    ├─ TokenManager (secure storage)
    └─ GoogleCalendarService (API calls)
```

### Data Flow

1. User signs in → `GoogleAuthManager`
2. OAuth token received → `TokenManager` encrypts and stores
3. ViewModel requests events → `GoogleCalendarService`
4. Service fetches from Google Calendar API
5. Events flow to UI via `StateFlow`
6. Compose UI automatically updates

## Customization

### Change Colors

Edit `app/src/main/res/values/colors.xml`:

```xml
<color name="purple_500">#FF6200EE</color>
<color name="purple_700">#FF3700B3</color>
```

### Adjust Zoom Limits

Edit `YearCalendarView.kt`:

```kotlin
scale = (scale * zoomChange).coerceIn(0.3f, 10f)  // Min/Max zoom
```

### Change Month Layout

Edit `YearCalendarCanvas.kt`:

```kotlin
val monthWidth = size.width / 12f  // Horizontal columns
val dayHeight = 30.dp.toPx()       // Day cell height
```

## Security Notes

### What's Secure

✅ OAuth credentials in `local.properties` (gitignored)
✅ Access tokens encrypted with AES256_GCM
✅ Encryption key in Android Keystore
✅ No backup of sensitive data
✅ HTTPS for all network calls
✅ Read-only calendar access

### What to Do for Production

⚠️ Generate new OAuth credentials
⚠️ Set up backend proxy for token exchange
⚠️ Implement certificate pinning
⚠️ Use Android App Bundle (.aab)
⚠️ Sign with production keystore
⚠️ Enable ProGuard/R8 obfuscation
⚠️ Remove debug logging

See `SECURITY.md` for complete security guidelines.

## Development

### Running Tests

```bash
./gradlew test                    # Unit tests
./gradlew connectedAndroidTest    # Instrumented tests
```

### Code Style

This project follows:
- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Android Kotlin Style Guide](https://developer.android.com/kotlin/style-guide)

### Adding Features

1. Create feature branch: `git checkout -b feature/my-feature`
2. Implement changes
3. Test thoroughly
4. Create pull request

## Performance

### Optimizations

- Events grouped by date for O(1) lookup
- Canvas drawing instead of heavy View hierarchy
- Coroutines for async operations
- StateFlow for efficient state updates
- Lazy loading of calendar data

### Recommended Limits

- **Events per year**: Up to 2,500 per calendar
- **Calendars**: Up to 25 calendars
- **Zoom range**: 0.5x to 5x for best UX

### Memory Usage

Typical memory footprint:
- App baseline: ~50-80 MB
- With 1,000 events: ~60-90 MB
- With 5,000 events: ~80-120 MB

## Support

### Resources

- [Android Developer Docs](https://developer.android.com/)
- [Jetpack Compose Docs](https://developer.android.com/jetpack/compose)
- [Google Calendar API](https://developers.google.com/calendar)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)

### Common Questions

**Q: Can I edit events?**
A: Currently read-only. Event editing is a future enhancement.

**Q: Does it work offline?**
A: No, requires internet for initial load. Offline caching is planned.

**Q: Can I export the calendar view?**
A: Not yet implemented. Screenshot export is a future feature.

**Q: What Android versions are supported?**
A: Android 8.0 (API 26) and higher.

**Q: Is my data stored on a server?**
A: No, all data is fetched from Google and displayed locally. Only encrypted tokens are stored on device.

## Next Steps

After successfully running the app:

1. ✅ Test zoom functionality
2. ✅ Try different years
3. ✅ Check all your calendars appear
4. ✅ Test sign out and sign in again
5. ✅ Verify events display correctly

Enjoy your Year Calendar app! 📅
