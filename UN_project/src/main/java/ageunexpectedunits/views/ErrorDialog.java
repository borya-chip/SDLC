package ageunexpectedunits.views;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dialog;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;

public final class ErrorDialog extends JDialog {
    private ErrorDialog(java.awt.Frame owner, String message) {
        super(owner, "Дата не существует", Dialog.ModalityType.APPLICATION_MODAL);
        setUndecorated(true);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        setResizable(false);
        setSize(820, 300);
        setLocationRelativeTo(owner);

        JPanel content = new RoundedPanel();
        content.setLayout(new BorderLayout(34, 0));
        content.setBorder(BorderFactory.createEmptyBorder(48, 44, 30, 48));

        content.add(new ErrorIcon(), BorderLayout.WEST);

        JPanel text = new JPanel(new BorderLayout(0, 16));
        text.setOpaque(false);
        JLabel title = new JLabel("Дата не существует");
        title.setFont(title.getFont().deriveFont(Font.BOLD, 24f));
        text.add(title, BorderLayout.NORTH);

        JLabel description = new JLabel(toHtml(message));
        description.setFont(description.getFont().deriveFont(Font.PLAIN, 21f));
        description.setForeground(new Color(76, 80, 87));
        text.add(description, BorderLayout.CENTER);
        content.add(text, BorderLayout.CENTER);

        JButton okButton = new RoundedButton("OK");
        okButton.setFont(okButton.getFont().deriveFont(Font.BOLD, 18f));
        okButton.setPreferredSize(new Dimension(124, 56));
        okButton.addActionListener(event -> dispose());
        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 0, 0));
        buttons.setOpaque(false);
        buttons.add(okButton);
        content.add(buttons, BorderLayout.SOUTH);

        setContentPane(content);
        getRootPane().setDefaultButton(okButton);
    }

    public static void show(java.awt.Frame owner, String message) {
        new ErrorDialog(owner, message).setVisible(true);
    }

    private static String toHtml(String message) {
        String escapedMessage = message.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>");
        return "<html>" + escapedMessage + "</html>";
    }

    private static final class RoundedPanel extends JPanel {
        private RoundedPanel() {
            setOpaque(false);
        }

        @Override
        protected void paintComponent(Graphics graphics) {
            Graphics2D graphics2D = (Graphics2D) graphics.create();
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            graphics2D.setColor(Color.WHITE);
            graphics2D.fillRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 18, 18);
            graphics2D.setColor(new Color(110, 121, 133));
            graphics2D.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 18, 18);
            graphics2D.dispose();
            super.paintComponent(graphics);
        }
    }

    private static final class ErrorIcon extends JPanel {
        private ErrorIcon() {
            setOpaque(false);
            setPreferredSize(new Dimension(82, 82));
        }

        @Override
        protected void paintComponent(Graphics graphics) {
            Graphics2D graphics2D = (Graphics2D) graphics.create();
            graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            graphics2D.setColor(new Color(230, 74, 78));
            graphics2D.fillOval(0, 0, 82, 82);
            graphics2D.setColor(Color.WHITE);
            graphics2D.setFont(getFont().deriveFont(Font.BOLD, 48f));
            graphics2D.drawString("!", 31, 59);
            graphics2D.dispose();
        }
    }

    private static final class RoundedButton extends JButton {
        private RoundedButton(String text) {
            super(text);
            setContentAreaFilled(false);
            setBorderPainted(false);
            setFocusPainted(false);
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
