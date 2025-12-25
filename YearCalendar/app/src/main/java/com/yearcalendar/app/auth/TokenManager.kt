package com.yearcalendar.app.auth

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "auth_prefs")

@Singleton
class TokenManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val encryptedPrefs = EncryptedSharedPreferences.create(
        context,
        "secure_auth_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    companion object {
        private const val KEY_ACCESS_TOKEN = "access_token"
        private const val KEY_REFRESH_TOKEN = "refresh_token"
        private const val KEY_TOKEN_EXPIRY = "token_expiry"
        private const val KEY_AUTH_CODE = "auth_code"
    }

    suspend fun saveAccessToken(token: String) {
        encryptedPrefs.edit().putString(KEY_ACCESS_TOKEN, token).apply()
    }

    fun getAccessToken(): String? {
        return encryptedPrefs.getString(KEY_ACCESS_TOKEN, null)
    }

    suspend fun saveRefreshToken(token: String) {
        encryptedPrefs.edit().putString(KEY_REFRESH_TOKEN, token).apply()
    }

    fun getRefreshToken(): String? {
        return encryptedPrefs.getString(KEY_REFRESH_TOKEN, null)
    }

    suspend fun saveAuthCode(code: String) {
        encryptedPrefs.edit().putString(KEY_AUTH_CODE, code).apply()
    }

    fun getAuthCode(): String? {
        return encryptedPrefs.getString(KEY_AUTH_CODE, null)
    }

    suspend fun saveTokenExpiry(expiry: Long) {
        encryptedPrefs.edit().putLong(KEY_TOKEN_EXPIRY, expiry).apply()
    }

    fun getTokenExpiry(): Long {
        return encryptedPrefs.getLong(KEY_TOKEN_EXPIRY, 0L)
    }

    fun isTokenExpired(): Boolean {
        val expiry = getTokenExpiry()
        return expiry < System.currentTimeMillis()
    }

    suspend fun clearTokens() {
        encryptedPrefs.edit().clear().apply()
    }
}
