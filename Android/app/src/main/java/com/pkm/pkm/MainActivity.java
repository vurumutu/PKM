package com.pkm.pkm;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {
    private int actualTrain; // state of radio button
    private int speed;
    private ProgressBar pg1;
    private ArrayAdapter<String> trainsAdapter;
    private TextView speedText;
    private SeekBar speedSeekBar;
    private List<Train> trains;
    private Retrofit.Builder builder;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        String ip = intent.getStringExtra("key");
        setContentView(R.layout.activity_main);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE,
                WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);

        pg1 = (ProgressBar) findViewById(R.id.progressBar);

        speedText = (TextView) findViewById(R.id.speed_text);
        speedSeekBar = (SeekBar) findViewById(R.id.speed_seekBar);
        speedSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                speed = (progress - 128);
                speedText.setText("Speed: " + speed);

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                for (Train train : trains) {
                    if (train.getTrain_identificator() == actualTrain) {
                        train.setVelocity(speed);
                        sendNetworkRequest(train);
                    }
                }
            }
        });

        Button stopBtn = (Button) findViewById(R.id.stop_btn);
        stopBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                speedSeekBar.setProgress(128);
                for (Train train : trains) {
                    if (train.getTrain_identificator() == actualTrain) {
                        train.setVelocity(speed);
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
                for (Train train : trains) {
                    train.setVelocity(0);
                    sendNetworkRequest(train);
                }

            }
        });

        Spinner trainsSpinner = (Spinner) findViewById(R.id.spinner);
        trainsAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, android.R.id.text1);
        trainsAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        trainsSpinner.setAdapter(trainsAdapter);
        // na poczatku zaznaczony jest zerowy element, musimy go odznaczyc zeby nie wyslac requesta na poczatku
        trainsSpinner.setSelection(0, false);


        Toast.makeText(getApplicationContext(),
                ip, Toast.LENGTH_SHORT).show();

        try{
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
                    //Collections.sort(trains, new TrainComparer());
                    pg1.setVisibility(View.INVISIBLE);
                    getWindow().clearFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
                    int cnt = 0;
                    for (Train train : trains) {
                        trainsAdapter.insert(Integer.toString(train.getTrain_identificator()), cnt);
                        cnt++;
                    }
                    trainsAdapter.notifyDataSetChanged();
                }

                @Override
                public void onFailure(Call<List<Train>> call, Throwable t) {
                    finish();
                    Toast.makeText(MainActivity.this, "Nie udało się pobrać listy pociągów", Toast.LENGTH_SHORT).show();
                }
            });
        }
        catch(IllegalArgumentException | NullPointerException e){
            Toast.makeText(MainActivity.this, "Niepoprawny adres IP", Toast.LENGTH_SHORT).show();
            finish();
        }
//        builder = new Retrofit.Builder()
//                .baseUrl(ip)
//                .addConverterFactory(GsonConverterFactory.create());

        trainsSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                actualTrain = Integer.parseInt(parentView.getSelectedItem().toString());
            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
                return;
            }

        });


    }

    private void sendNetworkRequest(Train train) {
        Retrofit retrofit = builder.build();
        TrainClient client = retrofit.create(TrainClient.class);
        //Call<Train> call = client.setTrainSpeed(String.valueOf(train.getTrain_identificator()), train);

        Call<Void> call = client.setTrainSpeed(new TrainPost(train.getId(), 1, train.getVelocity(), train.getTrain_identificator(), 1));
        call.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                //Toast.makeText(MainActivity.this, "request sent", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Toast.makeText(MainActivity.this, "request failed", Toast.LENGTH_SHORT).show();
            }
        });

    }
}

//    private void refreshTrains(){
//        Retrofit retrofit = builder.build();
//        TrainClient train = retrofit.create(TrainClient.class);
//        Call<List<Train>> call = train.handleTrains();
//
//        call.enqueue(new Callback<List<Train>>() {
//            @Override
//            public void onResponse(Call<List<Train>> call, Response<List<Train>> response) {
//                for(Train train : response.body()){ // dodajemy do listy tylko nowe pociagi
//                    insertUniqueTrain(train);
//                }
//                //Collections.sort(trains, new TrainComparer());
//
//                pg1.setVisibility(View.INVISIBLE);
//                getWindow().clearFlags(WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
//                addRadioButtons(trains.size());
//            }
//
//            @Override
//            public void onFailure(Call<List<Train>> call, Throwable t) {
//                finish(); // call previous activity
//                Toast.makeText(MainActivity.this, "Nie udało się odświeżyć pociągów", Toast.LENGTH_SHORT).show();
//            }
//        });
//
//    }
//
//    public void insertUniqueTrain(Train train) {
//        if(!contains(train)) {
//            trains.add(train);
//        }
//    }
//
//    private boolean contains(Train train) {
//        for(Train i : trains) {
//            // czy jest pociag o takim samym id
//            if(i.getTrain_identificator() == (train.getTrain_identificator())) {
//                return true;
//            }
//        }
//        return false;
//    }
