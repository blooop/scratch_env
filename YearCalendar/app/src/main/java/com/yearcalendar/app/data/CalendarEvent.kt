package com.yearcalendar.app.data

import java.time.LocalDate
import java.time.LocalDateTime

data class CalendarEvent(
    val id: String,
    val title: String,
    val startDateTime: LocalDateTime,
    val endDateTime: LocalDateTime,
    val isAllDay: Boolean,
    val color: String? = null,
    val calendarId: String
) {
    val startDate: LocalDate get() = startDateTime.toLocalDate()
    val endDate: LocalDate get() = endDateTime.toLocalDate()
}

data class CalendarInfo(
    val id: String,
    val summary: String,
    val backgroundColor: String?,
    val foregroundColor: String?
)
