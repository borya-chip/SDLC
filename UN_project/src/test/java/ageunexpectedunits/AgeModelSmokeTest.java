package ageunexpectedunits;

import ageunexpectedunits.controllers.AgeController;
import ageunexpectedunits.models.AgeModel;

import java.time.LocalDate;

public final class AgeModelSmokeTest {
    private AgeModelSmokeTest() {
    }

    public static void main(String[] args) {
        AgeModel model = new AgeModel();
        model.calculate(LocalDate.of(2000, 2, 29), LocalDate.of(2024, 2, 28));
        check(model.getResult().years() == 23, "years before leap-day birthday");
        check(model.getResult().months() == 12, "months before leap-day birthday");
        check(model.getResult().days() == 0, "days before leap-day birthday");

        model.calculate(LocalDate.of(2000, 2, 29), LocalDate.of(2024, 2, 29));
        check(model.getResult().years() == 24, "years on birthday");

        AgeController controller = new AgeController(model);
        controller.calculateAge("29", "2", "2024");
        check(model.getBirthDate().equals(LocalDate.of(2024, 2, 29)), "leap day");
        controller.calculateAge("28", "2", "1926");
        check(model.getBirthDate().equals(LocalDate.of(1926, 2, 28)), "minimum year");
        controller.calculateAge("31", "12", "2000");
        check(model.getBirthDate().equals(LocalDate.of(2000, 12, 31)), "controller input");

        expectFailure(() -> controller.calculateAge("31", "2", "2000"));
        expectFailure(() -> controller.calculateAge("29", "2", "1900"));
        expectFailure(() -> controller.calculateAge("29", "2", "2023"));
        expectFailure(() -> controller.calculateAge("31", "4", "2020"));
        expectFailure(() -> controller.calculateAge("1", "1", "1925"));
        System.out.println("AgeModelSmokeTest: OK");
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void expectFailure(Runnable action) {
        try {
            action.run();
            throw new AssertionError("Expected validation failure");
        } catch (IllegalArgumentException expected) {
            // Expected path.
        }
    }
}
