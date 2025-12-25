# Security Policy

## Secure Credential Management

This app implements multiple layers of security for protecting OAuth credentials and user data.

### Credential Storage

1. **OAuth Client Credentials**
   - Stored in `local.properties` (NOT committed to git)
   - Embedded in BuildConfig at compile time
   - Obfuscated in release builds via ProGuard

2. **Access/Refresh Tokens**
   - Encrypted using `EncryptedSharedPreferences`
   - AES256_GCM encryption scheme
   - MasterKey backed by Android Keystore
   - Automatically rotated on device

3. **Backup Exclusion**
   - Sensitive data excluded from Android backup
   - Data extraction rules prevent cloud backup
   - `android:allowBackup="false"` in manifest

### Best Practices Implemented

#### Authentication
- OAuth 2.0 with PKCE flow
- Server-side auth code exchange
- Secure token storage
- Automatic token refresh
- Proper session management

#### Network Security
- HTTPS-only communication
- Certificate validation
- No custom trust managers
- Proper SSL/TLS configuration

#### Code Security
- ProGuard obfuscation in release builds
- R8 code shrinking
- No hardcoded secrets in source
- Secure random number generation

#### Data Protection
- Minimal permission requests
- Read-only calendar access
- Encrypted local storage
- No sensitive data in logs

### Production Deployment Checklist

Before deploying to production:

- [ ] Generate new OAuth credentials for production
- [ ] Update `local.properties` with production credentials
- [ ] Create Android keystore for signing release builds
- [ ] Enable ProGuard/R8 optimization
- [ ] Remove debug logging
- [ ] Implement certificate pinning
- [ ] Add root detection (optional)
- [ ] Implement SafetyNet attestation (optional)
- [ ] Set up proper key rotation policy
- [ ] Configure OAuth consent screen
- [ ] Add rate limiting on API calls
- [ ] Implement proper error handling without leaking info
- [ ] Audit third-party dependencies
- [ ] Set up security monitoring
- [ ] Create incident response plan

### OAuth Security

#### Client Secret Handling

The current implementation includes the client secret in the app for demonstration purposes. For production:

**Option 1: Backend Proxy (Recommended)**
```
User → Android App → Your Backend → Google OAuth
```
- App sends auth code to your backend
- Backend exchanges code for tokens
- Backend manages refresh tokens
- App receives short-lived access tokens

**Option 2: PKCE Flow (Mobile Apps)**
```
Use Proof Key for Code Exchange (PKCE)
- No client secret needed
- Dynamic code verifier
- More secure for mobile apps
```

#### OAuth Scopes

Currently requested scopes:
- `https://www.googleapis.com/auth/calendar.readonly`
- `https://www.googleapis.com/auth/calendar.events.readonly`

These are minimal, read-only scopes. Never request more permissions than necessary.

### Secure Communication

All API calls use HTTPS:
- Google Calendar API: `https://www.googleapis.com/calendar/v3/`
- OAuth endpoints: `https://accounts.google.com/o/oauth2/`

### Data Minimization

The app only accesses:
- Calendar event titles
- Event start/end times
- Event colors
- Calendar names

No personal data is:
- Stored permanently (except encrypted tokens)
- Transmitted to third parties
- Used for analytics
- Shared with other apps

### Key Rotation

Tokens are automatically managed:
- Access tokens: 1-hour expiry (Google default)
- Refresh tokens: Used to obtain new access tokens
- Auth codes: Single-use, short-lived

### Incident Response

If credentials are compromised:

1. **Immediate Actions**
   - Revoke OAuth tokens in Google Cloud Console
   - Generate new client credentials
   - Update app with new credentials
   - Release emergency update

2. **User Notification**
   - Inform users of potential breach
   - Instruct users to revoke app access
   - Provide steps to secure accounts

3. **Investigation**
   - Identify source of compromise
   - Assess impact scope
   - Document findings
   - Implement additional safeguards

### Security Updates

Dependencies should be regularly updated:
- Android SDK
- Jetpack Compose
- Google Play Services
- Third-party libraries

Run security audits:
```bash
./gradlew dependencyCheckAnalyze
```

### Reporting Security Issues

If you discover a security vulnerability:

**DO NOT** open a public issue.

Instead:
1. Email: [security contact - add your email]
2. Include detailed description
3. Provide steps to reproduce
4. Suggest mitigation if possible

We will:
- Acknowledge within 48 hours
- Provide fix timeline
- Credit reporter (if desired)
- Coordinate disclosure

### Additional Resources

- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
- [OAuth 2.0 for Mobile Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Google Calendar API Security](https://developers.google.com/calendar/api/guides/auth)
- [OWASP Mobile Security](https://owasp.org/www-project-mobile-security/)

## Security Compliance

This app follows:
- OWASP Mobile Top 10 guidelines
- Android Security Best Practices
- Google OAuth 2.0 specifications
- General Data Protection Regulation (GDPR) principles

## Disclaimer

This is a demonstration application. For production use:
- Conduct thorough security audit
- Implement additional safeguards
- Consult security professionals
- Comply with relevant regulations
- Maintain proper documentation
