package com.example.hanotificationapp

import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)

        val settingsButton = findViewById<Button>(R.id.settingsButton)

        val prefs: SharedPreferences = getSharedPreferences("app_prefs", MODE_PRIVATE)

        var url = prefs.getString("saved_url", "https://www.google.com")!!

        if (!url.startsWith("http")) {
            url = "https://$url"
        }

        webView.webViewClient = WebViewClient()
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        webView.loadUrl(url)

        settingsButton.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
    }

    override fun onResume() {
        super.onResume()

        val prefs: SharedPreferences = getSharedPreferences("app_prefs", MODE_PRIVATE)

        var url = prefs.getString("saved_url", "https://www.google.com")!!

        if (!url.startsWith("http")) {
            url = "https://$url"
        }

        webView.loadUrl(url)
    }
}