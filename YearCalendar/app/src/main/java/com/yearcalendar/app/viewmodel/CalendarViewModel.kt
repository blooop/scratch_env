package com.yearcalendar.app.viewmodel

import android.content.Intent
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.yearcalendar.app.auth.GoogleAuthManager
import com.yearcalendar.app.auth.TokenManager
import com.yearcalendar.app.calendar.GoogleCalendarService
import com.yearcalendar.app.data.AuthState
import com.yearcalendar.app.data.CalendarUiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import javax.inject.Inject

@HiltViewModel
class CalendarViewModel @Inject constructor(
    private val authManager: GoogleAuthManager,
    private val tokenManager: TokenManager,
    private val calendarService: GoogleCalendarService
) : ViewModel() {

    private val _authState = MutableStateFlow<AuthState>(AuthState.Loading)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()

    private val _calendarState = MutableStateFlow<CalendarUiState>(CalendarUiState.Loading)
    val calendarState: StateFlow<CalendarUiState> = _calendarState.asStateFlow()

    private val _currentYear = MutableStateFlow(LocalDate.now().year)
    val currentYear: StateFlow<Int> = _currentYear.asStateFlow()

    init {
        checkAuthStatus()
    }

    private fun checkAuthStatus() {
        viewModelScope.launch {
            try {
                val account = authManager.getLastSignedInAccount()
                if (account != null && authManager.hasCalendarPermission()) {
                    _authState.value = AuthState.Authenticated(account.email ?: "Unknown")
                    loadCalendarEvents(_currentYear.value)
                } else {
                    _authState.value = AuthState.NotAuthenticated
                }
            } catch (e: Exception) {
                _authState.value = AuthState.Error(e.message ?: "Unknown error")
            }
        }
    }

    fun handleSignInResult(data: Intent?) {
        viewModelScope.launch {
            try {
                val account = authManager.handleSignInResult(data)
                if (account != null) {
                    // Save auth code securely
                    account.serverAuthCode?.let { code ->
                        tokenManager.saveAuthCode(code)
                    }
                    _authState.value = AuthState.Authenticated(account.email ?: "Unknown")
                    loadCalendarEvents(_currentYear.value)
                } else {
                    _authState.value = AuthState.Error("Failed to sign in")
                }
            } catch (e: Exception) {
                _authState.value = AuthState.Error(e.message ?: "Sign in failed")
            }
        }
    }

    fun signOut() {
        viewModelScope.launch {
            try {
                authManager.signOut()
                tokenManager.clearTokens()
                calendarService.clearService()
                _authState.value = AuthState.NotAuthenticated
                _calendarState.value = CalendarUiState.Loading
            } catch (e: Exception) {
                _authState.value = AuthState.Error(e.message ?: "Sign out failed")
            }
        }
    }

    fun loadCalendarEvents(year: Int) {
        viewModelScope.launch {
            try {
                _calendarState.value = CalendarUiState.Loading
                _currentYear.value = year

                val calendars = calendarService.getCalendars()
                val events = calendarService.getEventsForYear(year)

                _calendarState.value = CalendarUiState.Success(events, calendars)
            } catch (e: Exception) {
                e.printStackTrace()
                _calendarState.value = CalendarUiState.Error(
                    e.message ?: "Failed to load events"
                )
            }
        }
    }

    fun changeYear(year: Int) {
        loadCalendarEvents(year)
    }

    fun refreshEvents() {
        loadCalendarEvents(_currentYear.value)
    }
}
