package ageunexpectedunits.views;

import ageunexpectedunits.controllers.AgeController;
import ageunexpectedunits.models.AgeCalculationResult;
import ageunexpectedunits.models.AgeModel;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.RenderingHints;
import java.text.NumberFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

public final class MainForm extends JFrame {
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("dd.MM.yyyy");
    private static final Color PAGE_COLOR = new Color(241, 244, 248);
    private static final Color LINE_COLOR = new Color(218, 223, 229);
    private final AgeController controller;
    private final AgeModel model;
    private final JLabel birthDateValue = valueLabel();
    private final JLabel calendarAgeValue = valueLabel();
    private final JLabel monthsValue = valueLabel();
    private final JLabel daysValue = valueLabel();
    private final JLabel minutesValue = valueLabel();
    private final JLabel coffeeValue = valueLabel();
    private final JLabel seriesValue = valueLabel();
    private final JLabel feedValue = valueLabel();
    private final JLabel calculationNote = new JLabel();
    private LocalDate lastBirthDate;

    public MainForm(AgeController controller, AgeModel model) {
        this.controller = controller;
        this.model = model;
        this.model.addStateChangedListener(event -> renderModelState());
        setTitle("Возраст в неожиданных единицах");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setMinimumSize(new Dimension(880, 420));
        setSize(900, 430);
        setLocationRelativeTo(null);
        initializeControls();
    }

    private void initializeControls() {
        JPanel page = new JPanel(new GridBagLayout());
        page.setBackground(PAGE_COLOR);
        page.setBorder(BorderFactory.createEmptyBorder(8, 26, 20, 26));

        JPanel card = new RoundedPanel(12, new Color(110, 121, 133));
        card.setLayout(new BorderLayout(0, 18));
        card.setBorder(BorderFactory.createEmptyBorder(20, 34, 20, 34));

        JLabel header = new JLabel("Возраст в неожиданных единицах");
        header.setFont(header.getFont().deriveFont(Font.BOLD, 20f));
        card.add(header, BorderLayout.NORTH);

        JPanel values = new JPanel(new GridLayout(8, 1));
        values.setBackground(Color.WHITE);
        values.add(createRow("Дата рождения", birthDateValue, false, 382));
        values.add(createRow("Календарный возраст", calendarAgeValue, true, 382));
        values.add(createRow("Полных месяцев", monthsValue, true, 382));
        values.add(createRow("Дней", daysValue, true, 382));
        values.add(createRow("Минут", minutesValue, true, 382));
        values.add(createRow("Чашек кофе", coffeeValue, true, 382));
        values.add(createRow("Серий по 45 минут", seriesValue, true, 382));
        values.add(createRow("Км ленты соцсетей", feedValue, true, 382));
        card.add(values, BorderLayout.CENTER);

        JButton inputButton = new RoundedButton("Ввести данные");
        inputButton.setFont(inputButton.getFont().deriveFont(Font.BOLD));
        inputButton.setPreferredSize(new Dimension(168, 45));
        inputButton.setFocusPainted(false);
        inputButton.addActionListener(event -> openInputForm());
        calculationNote.setForeground(new Color(92, 100, 110));
        calculationNote.setText(calculationNoteText());
        JPanel footer = new JPanel(new BorderLayout());
        footer.setBackground(Color.WHITE);
        footer.add(calculationNote, BorderLayout.WEST);
        footer.add(inputButton, BorderLayout.EAST);
        card.add(footer, BorderLayout.SOUTH);

        GridBagConstraints cardConstraints = new GridBagConstraints();
        cardConstraints.fill = GridBagConstraints.BOTH;
        cardConstraints.weightx = 1.0;
        cardConstraints.weighty = 1.0;
        page.add(card, cardConstraints);
        setContentPane(page);
    }

    private static JPanel createRow(String title, JLabel value, boolean separator, int valueOffset) {
        JPanel row = new JPanel(new BorderLayout());
        row.setBackground(Color.WHITE);
        row.setBorder(BorderFactory.createCompoundBorder(
                separator ? BorderFactory.createMatteBorder(1, 0, 0, 0, LINE_COLOR)
                        : BorderFactory.createEmptyBorder(),
                BorderFactory.createEmptyBorder(3, 4, 3, 4)));
        JLabel titleLabel = new JLabel(title);
        titleLabel.setForeground(new Color(75, 82, 91));
        JPanel titleColumn = new JPanel(new BorderLayout());
        titleColumn.setBackground(Color.WHITE);
        titleColumn.setPreferredSize(new Dimension(valueOffset, 0));
        titleColumn.add(titleLabel, BorderLayout.WEST);
        row.add(titleColumn, BorderLayout.WEST);
        row.add(value, BorderLayout.CENTER);
        return row;
    }

    private static JLabel valueLabel() {
        JLabel label = new JLabel("—", SwingConstants.LEFT);
        label.setFont(label.getFont().deriveFont(Font.PLAIN, 16f));
        return label;
    }

    private void openInputForm() {
        InputForm inputForm = new InputForm(this, lastBirthDate);
        inputForm.setVisible(true);
        if (!inputForm.isConfirmed()) {
            return;
        }
        try {
            controller.calculateAge(inputForm.getDayText(), inputForm.getMonthText(), inputForm.getYearText());
        } catch (IllegalArgumentException exception) {
            ErrorDialog.show(this, exception.getMessage());
        }
    }

    private void renderModelState() {
        lastBirthDate = model.getBirthDate();
        AgeCalculationResult result = model.getResult();
        if (lastBirthDate == null || result == null) {
            return;
        }
        NumberFormat integerFormat = NumberFormat.getNumberInstance(Locale.forLanguageTag("ru-RU"));
        NumberFormat decimalFormat = NumberFormat.getNumberInstance(Locale.forLanguageTag("ru-RU"));
        decimalFormat.setMinimumFractionDigits(2);
        decimalFormat.setMaximumFractionDigits(2);
        birthDateValue.setText(DATE_FORMAT.format(lastBirthDate));
        calendarAgeValue.setText(formatAge(result.years(), result.months(), result.days()));
        monthsValue.setText(integerFormat.format((long) result.years() * 12 + result.months()));
        daysValue.setText(integerFormat.format(result.totalDays()));
        minutesValue.setText(integerFormat.format(result.totalMinutes()));
        coffeeValue.setText(integerFormat.format(result.coffeeCups()));
        seriesValue.setText(integerFormat.format(result.tvSeriesEpisodes()));
        feedValue.setText(decimalFormat.format(result.socialFeedKilometers()));
        calculationNote.setText(calculationNoteText());
    }

    private static String calculationNoteText() {
        return "Расчет на " + DATE_FORMAT.format(LocalDate.now())
                + "  •  2 чашки/день  •  300 м ленты/день";
    }

    private static String formatAge(int years, int months, int days) {
        return years + " " + wordForm(years, "год", "года", "лет") + " "
                + months + " " + wordForm(months, "месяц", "месяца", "месяцев") + " "
                + days + " " + wordForm(days, "день", "дня", "дней");
    }

    private static String wordForm(int value, String singular, String few, String many) {
        int lastTwoDigits = value % 100;
        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return many;
        }
        return switch (value % 10) {
            case 1 -> singular;
            case 2, 3, 4 -> few;
            default -> many;
        };
    }

    private static final class RoundedPanel extends JPanel {
        private final int radius;
        private final Color borderColor;

        private RoundedPanel(int radius, Color borderColor) {
            this.radius = radius;
            this.borderColor = borderColor;
            setOpaque(false);
        }

        @Override
        protected void paintComponent(Graphics graphics) {
            Graphics2D graphics2D = (Graphics2D) graphics.create();
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            graphics2D.setColor(Color.WHITE);
            graphics2D.fillRoundRect(0, 0, getWidth() - 1, getHeight() - 1, radius, radius);
            graphics2D.setColor(borderColor);
            graphics2D.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, radius, radius);
            graphics2D.dispose();
            super.paintComponent(graphics);
        }
    }

    private static final class RoundedButton extends JButton {
        private RoundedButton(String text) {
            super(text);
            setContentAreaFilled(false);
            setBorderPainted(false);
            setOpaque(false);
        }

        @Override
        protected void paintComponent(Graphics graphics) {
            Graphics2D graphics2D = (Graphics2D) graphics.create();
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            graphics2D.setColor(new Color(229, 239, 252));
            graphics2D.fillRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 10, 10);
            graphics2D.setColor(new Color(104, 142, 183));
            graphics2D.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 10, 10);
            graphics2D.dispose();
            super.paintComponent(graphics);
        }
    }
}
