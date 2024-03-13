import java.awt.Color;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class timer extends JFrame {

    private JLabel label;
    private int tempoRestante;
    private String icone = "tray-icon.png";

    public timer(int tempoInicial) {
        super("timer");
        this.tempoRestante = tempoInicial;

        setUndecorated(true);
        setBackground(new Color(0, 0, 0, 80));

        label = new JLabel(formatarTempo(tempoRestante), JLabel.CENTER);
        label.setForeground(Color.WHITE);

        add(label);
        setSize(50, 25);
        setLocation(0, 0);
        setAlwaysOnTop(true);
        setType(JFrame.Type.UTILITY);
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        setIconImage(new ImageIcon(icone).getImage());
        setResizable(false);
        setVisible(true);

        while (tempoRestante > 0) {
            try {
                Thread.sleep(1000);
                tempoRestante--;
                label.setText(formatarTempo(tempoRestante));
                if (tempoRestante == 0) {
                    label.setForeground(Color.RED);
                }
            } catch (InterruptedException ex) {
                ex.printStackTrace();
            }
        }
    }

    private String formatarTempo(int segundos) {
        int horas = segundos / 3600;
        int minutos = (segundos % 3600) / 60;
        int segundosRestantes = segundos % 60;
        return String.format("%02d:%02d:%02d", horas, minutos, segundosRestantes);
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Uso: java -cp TimerBandeja.jar TimerBandeja <tempo>");
            System.exit(1);
        }

        try {
            int tempoInicial = Integer.parseInt(args[0]);
            new timer(tempoInicial);
        } catch (NumberFormatException e) {
            System.out.println("O argumento deve ser um número inteiro.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
