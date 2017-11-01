package com.pkm.pkm;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import retrofit2.Retrofit;


public class LoginActivity extends AppCompatActivity {
    String ip;
    Button connectBtn;
    EditText inputIp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        connectBtn = (Button)findViewById(R.id.btn_connect);
        inputIp = (EditText) findViewById(R.id.input_ip);

        connectBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                ip = inputIp.getText().toString();
                Toast.makeText(getApplicationContext(),
                        "Connecting...",Toast.LENGTH_SHORT).show();
                Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                myIntent.putExtra("key", ip); //Optional parameters
                startActivity(myIntent);
            }
        });


    }
}
