package ageunexpectedunits;

import ageunexpectedunits.controllers.AgeController;
import ageunexpectedunits.models.AgeModel;
import ageunexpectedunits.views.MainForm;

import javax.swing.SwingUtilities;

public final class Program {
    private Program() {
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            AgeModel model = new AgeModel();
            AgeController controller = new AgeController(model);
            MainForm mainForm = new MainForm(controller, model);
            mainForm.setVisible(true);
        });
    }
}
