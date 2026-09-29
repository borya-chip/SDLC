package ageunexpectedunits.controllers;

import ageunexpectedunits.models.AgeModel;

import java.time.DateTimeException;
import java.time.LocalDate;

public final class AgeController {
    private static final int MINIMUM_BIRTH_YEAR = 1926;
    private final AgeModel model;

    public AgeController(AgeModel model) {
        this.model = model;
    }

    public void calculateAge(String dayText, String monthText, String yearText) {
        String enteredDate = formatEnteredDate(dayText, monthText, yearText);
        int day = parseInteger(dayText, enteredDate);
        int month = parseInteger(monthText, enteredDate);
        int year = parseInteger(yearText, enteredDate);
        int currentYear = LocalDate.now().getYear();

        if (year < MINIMUM_BIRTH_YEAR || year > currentYear) {
            throw new IllegalArgumentException(
                    "Допустимая дата рождения: с 01.01.1926 по текущую дату.\n"
                            + "Введено: " + enteredDate);
        }

        LocalDate birthDate;

        try {
            birthDate = LocalDate.of(year, month, day);
        } catch (DateTimeException exception) {
            throw new IllegalArgumentException(
                    "Проверьте день, месяц и год: " + enteredDate, exception);
        }

        LocalDate today = LocalDate.now();
        if (birthDate.isAfter(today)) {
            throw new IllegalArgumentException(
                    "Дата рождения не может быть в будущем.\nВведено: " + enteredDate);
        }

        model.calculate(birthDate, today);
    }

    private static int parseInteger(String text, String enteredDate) {
        try {
            return Integer.parseInt(text.trim());
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException(
                    "Проверьте день, месяц и год: " + enteredDate, exception);
        }
    }

    private static String formatEnteredDate(String dayText, String monthText, String yearText) {
        return String.join(".", dayText.trim(), monthText.trim(), yearText.trim());
    }
}
