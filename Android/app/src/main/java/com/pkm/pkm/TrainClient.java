package com.pkm.pkm;
import org.json.JSONObject;

import java.nio.ByteBuffer;
import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

/**
 * Created by Karol on 26.10.2017.
 */

public interface TrainClient {
    @GET("/trains/")
    Call<List<Train>> handleTrains();
    @GET("/train/{train}/")
    Call<Train> getTrainSpeed(@Path("train") Train train);
    @POST("/train/post/0/")
    Call<Void> setTrainSpeed(@Body TrainPost trains);

}
