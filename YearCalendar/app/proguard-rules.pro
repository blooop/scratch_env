# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Keep Google API client classes
-keep class com.google.api.** { *; }
-keep class com.google.** { *; }
-dontwarn com.google.**

# Keep OAuth classes
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**

# Keep BuildConfig
-keep class **.BuildConfig { *; }

# Keep data classes
-keep class com.yearcalendar.app.data.** { *; }
