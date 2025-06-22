package com.flexiusgpt.healthconnect

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.foundation.layout.padding

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            HealthDashboard()
        }
    }
}

@Composable
fun HealthDashboard() {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("HealthConnect Dashboard") })
        }
    ) { padding ->
        Text(
            "Coming soon: Live sync with backend JSON...",
            modifier = Modifier.padding(padding)
        )
    }
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    HealthDashboard()
}
