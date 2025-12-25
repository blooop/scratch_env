package com.yearcalendar.app.di

import android.content.Context
import com.yearcalendar.app.auth.GoogleAuthManager
import com.yearcalendar.app.auth.TokenManager
import com.yearcalendar.app.calendar.GoogleCalendarService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideGoogleAuthManager(
        @ApplicationContext context: Context
    ): GoogleAuthManager {
        return GoogleAuthManager(context)
    }

    @Provides
    @Singleton
    fun provideTokenManager(
        @ApplicationContext context: Context
    ): TokenManager {
        return TokenManager(context)
    }

    @Provides
    @Singleton
    fun provideGoogleCalendarService(
        @ApplicationContext context: Context,
        authManager: GoogleAuthManager
    ): GoogleCalendarService {
        return GoogleCalendarService(context, authManager)
    }
}
