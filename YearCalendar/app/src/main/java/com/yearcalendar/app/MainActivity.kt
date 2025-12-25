package com.yearcalendar.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel
import com.yearcalendar.app.data.AuthState
import com.yearcalendar.app.ui.screens.CalendarScreen
import com.yearcalendar.app.ui.screens.SignInScreen
import com.yearcalendar.app.ui.theme.YearCalendarTheme
import com.yearcalendar.app.viewmodel.CalendarViewModel
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    private val signInLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        viewModel.handleSignInResult(result.data)
    }

    private lateinit var viewModel: CalendarViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            viewModel = hiltViewModel()
            val authState by viewModel.authState.collectAsState()

            YearCalendarTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    when (authState) {
                        is AuthState.Loading -> {
                            SignInScreen(
                                onSignInClick = { /* Loading */ },
                                isLoading = true,
                                errorMessage = null
                            )
                        }
                        is AuthState.NotAuthenticated -> {
                            SignInScreen(
                                onSignInClick = { startSignIn() },
                                isLoading = false,
                                errorMessage = null
                            )
                        }
                        is AuthState.Authenticated -> {
                            CalendarScreen(
                                viewModel = viewModel,
                                onSignOut = { viewModel.signOut() }
                            )
                        }
                        is AuthState.Error -> {
                            SignInScreen(
                                onSignInClick = { startSignIn() },
                                isLoading = false,
                                errorMessage = (authState as AuthState.Error).message
                            )
                        }
                    }
                }
            }
        }
    }

    private fun startSignIn() {
        val authManager = (application as YearCalendarApplication).let {
            // Get auth manager through Hilt
            com.yearcalendar.app.auth.GoogleAuthManager(this)
        }
        signInLauncher.launch(authManager.getSignInIntent())
    }
}
