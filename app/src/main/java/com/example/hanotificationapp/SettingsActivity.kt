package com.example.webviewapp

import android.content.SharedPreferences
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class SettingsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        val urlInput = findViewById<EditText>(R.id.urlInput)
        val saveButton = findViewById<Button>(R.id.saveButton)

        val prefs: SharedPreferences = getSharedPreferences("app_prefs", MODE_PRIVATE)

        urlInput.setText(prefs.getString("saved_url", "https://www.google.com"))

        saveButton.setOnClickListener {
            val url = urlInput.text.toString()

            prefs.edit().putString("saved_url", url).apply()

            Toast.makeText(this, "URL Saved", Toast.LENGTH_SHORT).show()
            finish()
        }
    }
}