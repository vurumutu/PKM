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
    private int speed;

    public int getId() {
        return id;
    }

    public int getSpeed() {
        return speed;
    }

    public void setSpeed(int speed) {
        this.speed = speed;
    }

    public void setId(int id) {
        this.id = id;
    }
//    public String name;

}
