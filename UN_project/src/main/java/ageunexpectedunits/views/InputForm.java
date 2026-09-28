package ageunexpectedunits.views;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public final class InputForm extends JDialog {
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    private final JTextField dateTextField = new JTextField();
    private boolean confirmed;

    public InputForm(java.awt.Frame owner, LocalDate lastBirthDate) {
        super(owner, "Ввод даты рождения", true);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setResizable(false);
        setSize(860, 340);
        setLocationRelativeTo(owner);

        JPanel content = new JPanel(new BorderLayout(0, 20));
        content.setBackground(Color.WHITE);
        content.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(110, 121, 133)),
                BorderFactory.createEmptyBorder(42, 44, 40, 54)));

        JLabel title = new JLabel("Дата рождения в формате ДД.ММ.ГГГГ");
        title.setFont(title.getFont().deriveFont(Font.PLAIN, 22f));
        content.add(title, BorderLayout.NORTH);

        dateTextField.setFont(dateTextField.getFont().deriveFont(Font.PLAIN, 20f));
        dateTextField.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(137, 146, 157)),
                BorderFactory.createEmptyBorder(8, 16, 8, 16)));
        dateTextField.setPreferredSize(new Dimension(0, 58));
        JPanel fieldArea = new JPanel(new BorderLayout());
        fieldArea.setBackground(Color.WHITE);
        fieldArea.add(dateTextField, BorderLayout.NORTH);
        content.add(fieldArea, BorderLayout.CENTER);

        JButton okButton = new RoundedButton("OK", new Color(229, 239, 252), new Color(104, 142, 183));
        okButton.setFont(okButton.getFont().deriveFont(Font.BOLD));
        okButton.setPreferredSize(new Dimension(116, 50));
        okButton.addActionListener(event -> {
            confirmed = true;
            dispose();
        });

        JButton cancelButton = new RoundedButton("Отмена", new Color(250, 250, 250), new Color(145, 145, 145));
        cancelButton.setPreferredSize(new Dimension(126, 50));
        cancelButton.addActionListener(event -> dispose());

        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 18, 0));
        buttons.setBackground(Color.WHITE);
        buttons.add(okButton);
        buttons.add(cancelButton);
        content.add(buttons, BorderLayout.SOUTH);

        add(content);
        fillLastDate(lastBirthDate);
        getRootPane().setDefaultButton(okButton);
    }

    public boolean isConfirmed() {
        return confirmed;
    }

    public String getDayText() {
        return datePart(0);
    }

    public String getMonthText() {
        return datePart(1);
    }

    public String getYearText() {
        return datePart(2);
    }

    private String datePart(int index) {
        String[] parts = dateTextField.getText().trim().split("\\.", -1);
        return index < parts.length ? parts[index].trim() : "";
    }

    private void fillLastDate(LocalDate lastBirthDate) {
        if (lastBirthDate != null) {
            dateTextField.setText(DATE_FORMAT.format(lastBirthDate));
        }
    }

    private static final class RoundedButton extends JButton {
        private final Color fillColor;
        private final Color lineColor;

        private RoundedButton(String text, Color fillColor, Color lineColor) {
            super(text);
            this.fillColor = fillColor;
            this.lineColor = lineColor;
            setContentAreaFilled(false);
            setBorderPainted(false);
            setFocusPainted(false);
            setOpaque(false);
        }

        @Override
        protected void paintComponent(Graphics graphics) {
            Graphics2D graphics2D = (Graphics2D) graphics.create();
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            graphics2D.setColor(fillColor);
            graphics2D.fillRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 10, 10);
            graphics2D.setColor(lineColor);
            graphics2D.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 10, 10);
            graphics2D.dispose();
            super.paintComponent(graphics);
        }
    }
}
