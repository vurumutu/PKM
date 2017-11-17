package com.pkm.pkm;

import android.content.Intent;
import android.support.annotation.IdRes;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {
    private String ip;
    private int actualTrain; // state of radio button
    private int speed;
    private ProgressBar pg1;
    private RadioGroup radioGroup;
    private TextView speedText;
    private SeekBar speedSeekBar;
    private List<Train> trains;
    private Retrofit.Builder builder;
    //private ArrayList<Train> trainsTest;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        String ip = intent.getStringExtra("key");
        setContentView(R.layout.activity_main);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE,
                WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);

        pg1 = (ProgressBar) findViewById(R.id.progressBar);
        speedText = (TextView)findViewById(R.id.speed_text);
        speedSeekBar = (SeekBar) findViewById(R.id.speed_seekBar);
        speedSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                speed = (progress - 128); // handle negative velocities
                speedText.setText("Speed: " + speed);

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // iterate though array list and find actualTrain
                for (Train train: trains) {
                    if(train.getTrain_identificator() == actualTrain){
                        trains.get(actualTrain).setVelocity(speed);
                        sendNetworkRequest(train);
                    }
                }
            }
        });

        Button stopBtn = (Button) findViewById(R.id.stop_btn);
        stopBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //trains.get(actualTrain).setSpeed(0);
                speedSeekBar.setProgress(128);

                //could be handled by seekbar onStopTrackingTouch
                for (Train train: trains) {
                    if(train.getTrain_identificator() == actualTrain){
                        trains.get(actualTrain).setVelocity(speed);
                        sendNetworkRequest(train);
                    }
                }

            }
        });
        Button stopallBtn = (Button) findViewById(R.id.stopall_btn);
        stopallBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                speedSeekBar.setProgress(128);
                //send request for all items in trains
                for (Train train: trains) {
                    train.setVelocity(0);
                    sendNetworkRequest(train);
                }

            }
        });

        radioGroup = (RadioGroup)findViewById(R.id.radiogroup) ;
        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener(){
            @Override
            public void onCheckedChanged(RadioGroup group, @IdRes int checkedId) {

                RadioButton checkedRadioButton = (RadioButton) findViewById(checkedId);
                actualTrain = checkedRadioButton.getId() + 1;
                //Toast.makeText(getApplicationContext(), String.valueOf(actualTrain), Toast.LENGTH_SHORT).show();
                Log.d("radiobutton", String.valueOf(actualTrain));
            }
        });

        Toast.makeText(getApplicationContext(),
                ip, Toast.LENGTH_SHORT).show();
        //pg1.setVisibility(View.INVISIBLE);

        //for debug only
        //ip = "http://10.0.2.2:7777/";

        builder = new Retrofit.Builder()
                .baseUrl(ip)
                .addConverterFactory(GsonConverterFactory.create());

        Retrofit retrofit = builder.build();
        TrainClient train = retrofit.create(TrainClient.class);
        Call<List<Train>> call = train.handleTrains();

        call.enqueue(new Callback<List<Train>>() {
            @Override
            public void onResponse(Call<List<Train>> call, Response<List<Train>> response) {
                trains = response.body();
                // TODO check if trains exists
                pg1.setVisibility(View.INVISIBLE);
                getWindow().clearFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
                addRadioButtons(trains.size()); // replace with trains.size()
            }

            @Override
            public void onFailure(Call<List<Train>> call, Throwable t) {
                finish(); // call previous activity
                Toast.makeText(MainActivity.this, "Could not load trains", Toast.LENGTH_SHORT).show();
            }
        });
    }
    private void sendNetworkRequest(Train train){
        Retrofit retrofit = builder.build();
        TrainClient client = retrofit.create(TrainClient.class);
        Call<Train> call = client.setTrainSpeed(String.valueOf(train.getTrain_identificator()), train);
        call.enqueue(new Callback<Train>() {
            @Override
            public void onResponse(Call<Train> call, Response<Train> response) {
                //Toast.makeText(MainActivity.this, "request sent", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<Train> call, Throwable t) {
                Toast.makeText(MainActivity.this, "sending request failed", Toast.LENGTH_SHORT).show();
            }
        });

    }

    public void addRadioButtons(int num) {

        RadioGroup rg = (RadioGroup) findViewById(R.id.radiogroup);
        rg.setOrientation(RadioGroup.VERTICAL);
        final RadioButton[] rb = new RadioButton[num];
        for(int i = 0; i < num; i++)
        {
            rb[i]  = new RadioButton(this);
            rg.addView(rb[i]);
            rb[i].setId(i);
            rb[i].setText("Train " + (i+1));

        }
        rb[0].setChecked(true);
    }

}
