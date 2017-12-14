package com.pkm.pkm;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

/**
 * Created by Karol on 26.10.2017.
 */

public class Train{

    private int id;
    private int velocity;
    public int train_identificator;
    private int position;
    private int track_number;

    public int getId() {
        return id;
    }

    public int getVelocity() {
        return velocity;
    }

    public int getPosition() {
        return position;
    }

    public int getTrack_number() {
        return track_number;
    }


    public void setVelocity(int velocity) {
        this.velocity = velocity;
    }

    public int getTrain_identificator() {
        return train_identificator;
    }

    public Train(int id, int velocity, int train_identificator, int posotion, int track_number) {
        this.id = id;
        this.velocity = velocity;
        this.train_identificator = train_identificator;
        this.position = posotion;
        this.track_number = track_number;
    }


}
