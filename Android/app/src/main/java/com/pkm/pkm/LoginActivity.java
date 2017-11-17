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


    public static Boolean containsIP(String s) {
        java.util.regex.Matcher m = java.util.regex.Pattern.compile(
                "(?<!\\d|\\d\\.)" +
                        "(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                        "(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                        "(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                        "(?:[01]?\\d\\d?|2[0-4]\\d|25[0-5])" +
                        "(?!\\d|\\.\\d)").matcher(s);
        return m.find() ? Boolean.TRUE : Boolean.FALSE;
    }
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
                if(containsIP(ip)){
                    if(!ip.contains("http://")){
                        ip = "http://" + ip;
                    }
                    Toast.makeText(getApplicationContext(),
                            ("Connecting to " + ip), Toast.LENGTH_SHORT).show();
                    Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                    myIntent.putExtra("key", ip); //Optional parameters
                    startActivity(myIntent);
                }
                else {
                    Toast.makeText(getApplicationContext(),
                            ("Wrong ip format"), Toast.LENGTH_SHORT).show();
                }
            }
        });


    }
}
