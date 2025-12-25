# Year Calendar for Android

A modern Android app that displays your Google Calendar in an elegant year view with zoom and pan capabilities.

## Features

- **Year View**: See your entire year at a glance with months displayed as vertical columns
- **Zoom & Pan**: Smoothly zoom in to see details or zoom out to see the whole year
- **Secure Authentication**: OAuth 2.0 integration with Google for secure calendar access
- **Event Display**: Color-coded events from all your Google calendars
- **Material Design 3**: Modern UI using Jetpack Compose
- **Encrypted Storage**: Credentials stored securely using Android's EncryptedSharedPreferences

## Technology Stack

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose with Material Design 3
- **Architecture**: MVVM with Hilt for dependency injection
- **Authentication**: Google Sign-In with OAuth 2.0
- **API**: Google Calendar API v3
- **Security**:
  - EncryptedSharedPreferences for token storage
  - BuildConfig for API keys (not committed to version control)
  - Secure credential management with MasterKey encryption

## Setup Instructions

### Prerequisites

1. Android Studio (latest version recommended)
2. Android SDK 26 or higher
3. Google Cloud Project with Calendar API enabled

### Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project: `year-calendar-482211`
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Add authorized redirect URIs
5. Download the credentials

### OAuth Configuration

The OAuth credentials should be configured in `local.properties`. This file should contain:

```properties
google.client.id=YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com
google.client.secret=YOUR_GOOGLE_CLIENT_SECRET
google.project.id=your-project-id
```

**Note:** The actual OAuth credentials have been provided separately and should be added to your `local.properties` file.

**IMPORTANT**: For production deployment:
1. **Never commit `local.properties` to version control** (already in .gitignore)
2. Generate new OAuth credentials for production
3. Use Android keystore for release builds
4. Consider using Firebase Remote Config or similar for credential management
5. Implement certificate pinning for additional security

### Building the App

1. Clone this repository
2. Open the project in Android Studio
3. Ensure `local.properties` contains your OAuth credentials
4. Sync Gradle files
5. Build and run on an emulator or physical device

```bash
./gradlew assembleDebug
```

### Running the App

1. Launch the app on your device
2. Tap "Sign in with Google"
3. Authorize calendar access
4. View your calendar in year format
5. Use pinch-to-zoom or the zoom buttons to scale the view
6. Pan around to navigate different months

## Security Features

### Credential Protection

1. **Local Storage**: OAuth credentials stored in `local.properties` (gitignored)
2. **Encrypted Tokens**: Access/refresh tokens encrypted using AES256_GCM
3. **MasterKey**: Android Keystore-backed encryption
4. **No Backup**: Sensitive data excluded from device backups
5. **BuildConfig**: API keys embedded in BuildConfig (obfuscated in release builds)
6. **ProGuard**: Release builds use code obfuscation

### Authentication Flow

1. User initiates sign-in
2. Google OAuth 2.0 authorization
3. Server auth code received
4. Tokens encrypted and stored locally
5. Calendar API access via authenticated service
6. Automatic token refresh handling

### Permissions

The app requests minimal permissions:
- `INTERNET`: Required for API calls
- `ACCESS_NETWORK_STATE`: Check connectivity
- Calendar scopes: Read-only access to calendar events

## Architecture

### Project Structure

```
app/
├── auth/
│   ├── GoogleAuthManager.kt      # Handles Google Sign-In
│   └── TokenManager.kt            # Secure token storage
├── calendar/
│   └── GoogleCalendarService.kt  # Calendar API integration
├── data/
│   ├── CalendarEvent.kt          # Data models
│   └── AuthState.kt              # UI state models
├── di/
│   └── AppModule.kt              # Hilt dependency injection
├── ui/
│   ├── components/
│   │   └── YearCalendarView.kt   # Main calendar view with zoom
│   ├── screens/
│   │   ├── SignInScreen.kt       # Authentication screen
│   │   └── CalendarScreen.kt     # Main calendar screen
│   └── theme/
│       ├── Theme.kt              # Material theme
│       └── Type.kt               # Typography
├── viewmodel/
│   └── CalendarViewModel.kt      # Business logic
└── MainActivity.kt               # Entry point
```

### Design Patterns

- **MVVM**: Separation of concerns between UI and business logic
- **Repository Pattern**: Calendar service acts as data source
- **Dependency Injection**: Hilt manages dependencies
- **State Management**: StateFlow for reactive UI updates
- **Single Activity**: Compose navigation pattern

## Customization

### Changing Colors

Edit `app/src/main/res/values/colors.xml` and `ui/theme/Theme.kt`

### Adjusting Zoom Limits

In `YearCalendarView.kt`, modify the zoom constraints:

```kotlin
scale = (scale * zoomChange).coerceIn(0.5f, 5f)  // Min 0.5x, Max 5x
```

### Event Display

Customize event indicators in `YearCalendarCanvas` function within `YearCalendarView.kt`

## Known Limitations

1. **Read-Only**: Currently displays events but doesn't support editing
2. **Event Details**: Tap to view event details not yet implemented
3. **Offline Mode**: Requires internet connection for initial load
4. **Large Datasets**: Performance may degrade with thousands of events

## Future Enhancements

- [ ] Event detail view on tap
- [ ] Offline caching with Room database
- [ ] Event creation and editing
- [ ] Multiple calendar filtering
- [ ] Dark mode support
- [ ] Widget for home screen
- [ ] Export calendar view as image
- [ ] Recurring event optimization

## Troubleshooting

### Sign-In Fails

- Verify OAuth credentials in `local.properties`
- Check that Calendar API is enabled in Google Cloud Console
- Ensure SHA-1 fingerprint is registered for Android app

### No Events Displayed

- Confirm calendar permissions granted
- Check network connectivity
- Verify calendars have events in the selected year

### Build Errors

- Clean and rebuild: `./gradlew clean build`
- Invalidate caches in Android Studio
- Check Gradle JDK version (17 recommended)

## License

This project is provided as-is for demonstration purposes.

## Security Disclosure

If you discover a security vulnerability, please email the project maintainer rather than using the issue tracker.

## Contributing

Contributions are welcome! Please ensure:
1. Code follows Kotlin coding conventions
2. New features include appropriate tests
3. Security best practices are maintained
4. No sensitive credentials in commits
