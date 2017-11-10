package com.pkm.pkm;
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
    @GET("/trains")
    Call<List<Train>> handleTrains();
    @GET("trains/{train}")
    Call<Train> getTrainSpeed(@Path("train") String train);
    @PUT("trains/{train}")
    Call<Train> setTrainSpeed(@Path("train") String train, @Body Train trains);

}
