package com.yearcalendar.app.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.rememberTransformableState
import androidx.compose.foundation.gestures.transformable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ZoomIn
import androidx.compose.material.icons.filled.ZoomOut
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.yearcalendar.app.data.CalendarEvent
import java.time.LocalDate
import java.time.YearMonth
import java.time.format.TextStyle as JavaTextStyle
import java.util.Locale
import kotlin.math.max
import kotlin.math.min

@Composable
fun YearCalendarView(
    year: Int,
    events: List<CalendarEvent>,
    modifier: Modifier = Modifier
) {
    var scale by remember { mutableStateOf(1f) }
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }

    val transformableState = rememberTransformableState { zoomChange, panChange, _ ->
        scale = (scale * zoomChange).coerceIn(0.5f, 5f)
        offsetX += panChange.x
        offsetY += panChange.y
    }

    Box(modifier = modifier) {
        // Main calendar canvas
        YearCalendarCanvas(
            year = year,
            events = events,
            scale = scale,
            offsetX = offsetX,
            offsetY = offsetY,
            modifier = Modifier
                .fillMaxSize()
                .transformable(state = transformableState)
        )

        // Zoom controls
        Column(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            FloatingActionButton(
                onClick = { scale = (scale * 1.2f).coerceAtMost(5f) },
                containerColor = MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier.size(48.dp)
            ) {
                Icon(Icons.Default.ZoomIn, "Zoom In")
            }
            Spacer(modifier = Modifier.height(8.dp))
            FloatingActionButton(
                onClick = { scale = (scale / 1.2f).coerceAtLeast(0.5f) },
                containerColor = MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier.size(48.dp)
            ) {
                Icon(Icons.Default.ZoomOut, "Zoom Out")
            }
            Spacer(modifier = Modifier.height(8.dp))
            FloatingActionButton(
                onClick = {
                    scale = 1f
                    offsetX = 0f
                    offsetY = 0f
                },
                containerColor = MaterialTheme.colorScheme.secondaryContainer,
                modifier = Modifier.size(48.dp)
            ) {
                Text("1x", fontSize = 12.sp)
            }
        }
    }
}

@Composable
fun YearCalendarCanvas(
    year: Int,
    events: List<CalendarEvent>,
    scale: Float,
    offsetX: Float,
    offsetY: Float,
    modifier: Modifier = Modifier
) {
    val textMeasurer = rememberTextMeasurer()
    val primaryColor = MaterialTheme.colorScheme.primary
    val onSurfaceColor = MaterialTheme.colorScheme.onSurface
    val surfaceVariantColor = MaterialTheme.colorScheme.surfaceVariant
    val backgroundColor = MaterialTheme.colorScheme.background

    // Group events by date for efficient lookup
    val eventsByDate = remember(events) {
        events.groupBy { it.startDate }
    }

    Canvas(
        modifier = modifier
            .background(backgroundColor)
            .graphicsLayer(
                scaleX = scale,
                scaleY = scale,
                translationX = offsetX,
                translationY = offsetY
            )
    ) {
        val monthWidth = size.width / 12f
        val dayHeight = 30.dp.toPx()
        val headerHeight = 40.dp.toPx()

        // Draw each month as a vertical column
        for (month in 1..12) {
            val yearMonth = YearMonth.of(year, month)
            val daysInMonth = yearMonth.lengthOfMonth()
            val monthName = yearMonth.month.getDisplayName(JavaTextStyle.SHORT, Locale.getDefault())
            val x = (month - 1) * monthWidth

            // Draw month header
            drawRect(
                color = primaryColor,
                topLeft = Offset(x, 0f),
                size = Size(monthWidth, headerHeight)
            )

            drawText(
                textMeasurer = textMeasurer,
                text = monthName,
                topLeft = Offset(x + monthWidth / 2 - 20.dp.toPx(), 10.dp.toPx()),
                style = TextStyle(
                    color = Color.White,
                    fontSize = 14.sp
                )
            )

            // Draw days
            for (day in 1..daysInMonth) {
                val date = LocalDate.of(year, month, day)
                val y = headerHeight + (day - 1) * dayHeight
                val isWeekend = date.dayOfWeek.value >= 6
                val isToday = date == LocalDate.now()

                // Day background
                drawRect(
                    color = when {
                        isToday -> primaryColor.copy(alpha = 0.3f)
                        isWeekend -> surfaceVariantColor.copy(alpha = 0.5f)
                        else -> Color.Transparent
                    },
                    topLeft = Offset(x, y),
                    size = Size(monthWidth, dayHeight)
                )

                // Day border
                drawLine(
                    color = onSurfaceColor.copy(alpha = 0.1f),
                    start = Offset(x, y),
                    end = Offset(x + monthWidth, y),
                    strokeWidth = 1.dp.toPx()
                )

                // Vertical border
                if (month < 12) {
                    drawLine(
                        color = onSurfaceColor.copy(alpha = 0.2f),
                        start = Offset(x + monthWidth, y),
                        end = Offset(x + monthWidth, y + dayHeight),
                        strokeWidth = 1.dp.toPx()
                    )
                }

                // Day number
                drawText(
                    textMeasurer = textMeasurer,
                    text = day.toString(),
                    topLeft = Offset(x + 4.dp.toPx(), y + 4.dp.toPx()),
                    style = TextStyle(
                        color = if (isToday) primaryColor else onSurfaceColor,
                        fontSize = 12.sp
                    )
                )

                // Draw events for this day
                val dayEvents = eventsByDate[date] ?: emptyList()
                if (dayEvents.isNotEmpty()) {
                    val eventIndicatorSize = 6.dp.toPx()
                    val maxIndicators = ((monthWidth - 30.dp.toPx()) / (eventIndicatorSize + 2.dp.toPx())).toInt()
                    val eventsToShow = min(dayEvents.size, maxIndicators)

                    for (i in 0 until eventsToShow) {
                        val event = dayEvents[i]
                        val eventColor = parseEventColor(event.color) ?: primaryColor
                        val indicatorX = x + 25.dp.toPx() + i * (eventIndicatorSize + 2.dp.toPx())
                        val indicatorY = y + 8.dp.toPx()

                        drawCircle(
                            color = eventColor,
                            radius = eventIndicatorSize / 2,
                            center = Offset(indicatorX, indicatorY)
                        )
                    }

                    // Show "+X more" if there are more events
                    if (dayEvents.size > maxIndicators) {
                        val moreText = "+${dayEvents.size - maxIndicators}"
                        drawText(
                            textMeasurer = textMeasurer,
                            text = moreText,
                            topLeft = Offset(x + monthWidth - 20.dp.toPx(), y + 4.dp.toPx()),
                            style = TextStyle(
                                color = onSurfaceColor.copy(alpha = 0.6f),
                                fontSize = 8.sp
                            )
                        )
                    }
                }
            }
        }
    }
}

private fun parseEventColor(colorString: String?): Color? {
    if (colorString == null) return null
    return try {
        if (colorString.startsWith("#")) {
            Color(android.graphics.Color.parseColor(colorString))
        } else {
            // Handle numeric color IDs from Google Calendar
            when (colorString) {
                "1" -> Color(0xFFAC725E)
                "2" -> Color(0xFFD06B64)
                "3" -> Color(0xFFF83A22)
                "4" -> Color(0xFFFA573C)
                "5" -> Color(0xFFFF6B08)
                "6" -> Color(0xFFFFB878)
                "7" -> Color(0xFFFBD75B)
                "8" -> Color(0xFFFBF475)
                "9" -> Color(0xFFDBDB77)
                "10" -> Color(0xFF51B749)
                "11" -> Color(0xFF42D692)
                else -> null
            }
        }
    } catch (e: Exception) {
        null
    }
}
