package com.yearcalendar.app.calendar

import android.content.Context
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential
import com.google.api.client.http.javanet.NetHttpTransport
import com.google.api.client.json.gson.GsonFactory
import com.google.api.client.util.DateTime
import com.google.api.services.calendar.Calendar
import com.google.api.services.calendar.CalendarScopes
import com.yearcalendar.app.auth.GoogleAuthManager
import com.yearcalendar.app.data.CalendarEvent
import com.yearcalendar.app.data.CalendarInfo
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneId
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class GoogleCalendarService @Inject constructor(
    @ApplicationContext private val context: Context,
    private val authManager: GoogleAuthManager
) {
    private var calendarService: Calendar? = null

    private fun initializeCalendarService(): Calendar? {
        val account = authManager.getLastSignedInAccount() ?: return null

        val credential = GoogleAccountCredential.usingOAuth2(
            context,
            listOf(CalendarScopes.CALENDAR_READONLY, CalendarScopes.CALENDAR_EVENTS_READONLY)
        )
        credential.selectedAccount = account.account

        return Calendar.Builder(
            NetHttpTransport(),
            GsonFactory.getDefaultInstance(),
            credential
        )
            .setApplicationName("Year Calendar")
            .build()
    }

    suspend fun getCalendars(): List<CalendarInfo> = withContext(Dispatchers.IO) {
        try {
            val service = calendarService ?: initializeCalendarService() ?: return@withContext emptyList()
            calendarService = service

            val calendarList = service.calendarList().list().execute()
            calendarList.items?.map { calendar ->
                CalendarInfo(
                    id = calendar.id,
                    summary = calendar.summary ?: "Unknown",
                    backgroundColor = calendar.backgroundColor,
                    foregroundColor = calendar.foregroundColor
                )
            } ?: emptyList()
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    suspend fun getEventsForYear(year: Int): List<CalendarEvent> = withContext(Dispatchers.IO) {
        try {
            val service = calendarService ?: initializeCalendarService() ?: return@withContext emptyList()
            calendarService = service

            val timeZone = ZoneId.systemDefault()
            val startOfYear = LocalDateTime.of(year, 1, 1, 0, 0)
            val endOfYear = LocalDateTime.of(year, 12, 31, 23, 59)

            val timeMin = DateTime(startOfYear.atZone(timeZone).toInstant().toEpochMilli())
            val timeMax = DateTime(endOfYear.atZone(timeZone).toInstant().toEpochMilli())

            val calendars = getCalendars()
            val allEvents = mutableListOf<CalendarEvent>()

            for (calendar in calendars) {
                try {
                    val events = service.events().list(calendar.id)
                        .setTimeMin(timeMin)
                        .setTimeMax(timeMax)
                        .setOrderBy("startTime")
                        .setSingleEvents(true)
                        .setMaxResults(2500)
                        .execute()

                    events.items?.forEach { event ->
                        val start = event.start?.dateTime ?: event.start?.date
                        val end = event.end?.dateTime ?: event.end?.date

                        if (start != null && end != null) {
                            val startDateTime = parseDateTime(start.value)
                            val endDateTime = parseDateTime(end.value)

                            allEvents.add(
                                CalendarEvent(
                                    id = event.id,
                                    title = event.summary ?: "Untitled",
                                    startDateTime = startDateTime,
                                    endDateTime = endDateTime,
                                    isAllDay = event.start.dateTime == null,
                                    color = event.colorId ?: calendar.backgroundColor,
                                    calendarId = calendar.id
                                )
                            )
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }

            allEvents.sortedBy { it.startDateTime }
        } catch (e: Exception) {
            e.printStackTrace()
            emptyList()
        }
    }

    private fun parseDateTime(value: Long): LocalDateTime {
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(value), ZoneId.systemDefault())
    }

    fun clearService() {
        calendarService = null
    }
}
