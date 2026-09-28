package ageunexpectedunits.models;

public record AgeCalculationResult(
        int years,
        int months,
        int days,
        long totalDays,
        long totalMinutes,
        long coffeeCups,
        long tvSeriesEpisodes,
        double socialFeedKilometers) {
}
