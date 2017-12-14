package com.pkm.pkm;

/**
 * Created by Karol on 14.12.2017.
 */

public class TrainPost {
    private int id;
    private int device_type;

    public TrainPost(int id, int device_type, int velocity, int train_identificator, int was_carried_out) {
        this.id = id;
        this.device_type = device_type;
        this.velocity = velocity;
        this.train_identificator = train_identificator;
        this.was_carried_out = was_carried_out;
    }

    private int velocity;
    private int train_identificator;
    private int was_carried_out;
}
