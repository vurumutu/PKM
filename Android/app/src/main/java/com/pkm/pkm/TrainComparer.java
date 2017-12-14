package com.pkm.pkm;

import java.util.Comparator;

/**
 * Created by Karol on 12.12.2017.
 */

public class TrainComparer implements Comparator<Train> {
    @Override
    public int compare(Train x, Train y) {
        // TODO: Handle null x or y values
        int startComparison = compare(x.train_identificator, y.train_identificator);
        return startComparison != 0 ? startComparison
                : compare(x.train_identificator, y.train_identificator);
    }

    private static int compare(int a, int b) {
        return a < b ? -1
                : a > b ? 1
                : 0;
    }
}
