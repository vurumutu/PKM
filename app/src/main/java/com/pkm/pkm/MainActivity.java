package com.pkm.pkm;

import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final TextView tv1 = (TextView)findViewById(R.id.textView);
        HttpGetRequest asyncGet = new HttpGetRequest(new AsyncResponse() {
            @Override
            public void processFinish(Object output) {
                Log.d("response asyncGet: ", (String) output);
                tv1.setText((String)output);
            }
        });
        asyncGet.execute("https://github-calendar.herokuapp.com/total/KaDw");
    }


}
