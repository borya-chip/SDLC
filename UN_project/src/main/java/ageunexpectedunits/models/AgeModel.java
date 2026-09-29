package ageunexpectedunits.models;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

public final class AgeModel {
    private static final double AVERAGE_COFFEE_CUPS_PER_DAY = 2.0;
    private static final double AVERAGE_SERIES_MINUTES_PER_DAY = 90.0;
    private static final double AVERAGE_EPISODE_MINUTES = 45.0;
    private static final double AVERAGE_SOCIAL_FEED_KILOMETERS_PER_DAY = 0.3;

    private final PropertyChangeSupport changes = new PropertyChangeSupport(this);
    private LocalDate birthDate;
    private AgeCalculationResult result;

    public LocalDate getBirthDate() {
        return birthDate;
    }

    public AgeCalculationResult getResult() {
        return result;
    }

    public void addStateChangedListener(PropertyChangeListener listener) {
        changes.addPropertyChangeListener("state", listener);
    }

    public void calculate(LocalDate birthDateInput, LocalDate today) {
        if (birthDateInput.isAfter(today)) {
            throw new IllegalArgumentException("Дата рождения не может быть в будущем.");
        }

        this.birthDate = birthDateInput;

        int years = today.getYear() - birthDateInput.getYear();
        if (birthDateInput.plusYears(years).isAfter(today)) {
            years--;
        }

        LocalDate afterYears = birthDateInput.plusYears(years);
        int months = 0;
        while (!afterYears.plusMonths(months + 1L).isAfter(today)) {
            months++;
        }

        LocalDate afterMonths = afterYears.plusMonths(months);
        int days = (int) ChronoUnit.DAYS.between(afterMonths, today);
        long totalDays = Math.max(0L, ChronoUnit.DAYS.between(birthDateInput, today));
        long totalMinutes = totalDays * 24L * 60L;

        result = new AgeCalculationResult(
                years,
                months,
                days,
                totalDays,
                totalMinutes,
                Math.round(totalDays * AVERAGE_COFFEE_CUPS_PER_DAY),
                Math.round(totalDays * AVERAGE_SERIES_MINUTES_PER_DAY / AVERAGE_EPISODE_MINUTES),
                Math.round(totalDays * AVERAGE_SOCIAL_FEED_KILOMETERS_PER_DAY * 100.0) / 100.0);

        changes.firePropertyChange("state", null, result);
    }
}
