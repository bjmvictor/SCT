import java.awt.Color;
import java.io.IOException;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Temporizador extends JFrame {

    private JLabel label;
    private int tempoRestante = 10;//(3 * 60 * 60); // tempo em segundos
    private String icone = "tray-icon.png";

    public Temporizador() {  
        super("Temporizador");
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
                    enviarMensagemDesligarComputador();
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

    private void enviarMensagemDesligarComputador() throws InterruptedException {
        int tentativas = 3;
        while (tentativas > 0) {
            try {
                enviarMensagem();
                Thread.sleep(30000);
                desligarComputador();
                break;
            } catch (IOException e) {
                e.printStackTrace();
                tentativas--;
                System.out.println("Tentando novamente em 5 segundos...");
                Thread.sleep(5000);
            }
        }
    }

    private void enviarMensagem() throws IOException {
        Runtime.getRuntime().exec("msg * O computador será desligado em 30 segundos!");
    }

    private void desligarComputador() throws IOException {
        Runtime.getRuntime().exec("shutdown -s -f -t 0");
    }

    public static void main(String[] args) {
        int tentativas = 3;
        while (tentativas > 0) {
            try {
                new Temporizador();
                Runtime.getRuntime().exec("net user bergson /active:no"); 
                break;
            } catch (Exception e) {
                e.printStackTrace();
                tentativas--;
                System.out.println("Tentando novamente em 5 segundos...");
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                }
            }
        }
    }
}
