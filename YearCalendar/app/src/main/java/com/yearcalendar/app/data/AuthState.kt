package com.yearcalendar.app.data

sealed class AuthState {
    object Loading : AuthState()
    object NotAuthenticated : AuthState()
    data class Authenticated(val email: String) : AuthState()
    data class Error(val message: String) : AuthState()
}

sealed class CalendarUiState {
    object Loading : CalendarUiState()
    data class Success(val events: List<CalendarEvent>, val calendars: List<CalendarInfo>) : CalendarUiState()
    data class Error(val message: String) : CalendarUiState()
}
