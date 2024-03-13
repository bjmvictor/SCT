import java.io.IOException;

public class Temporizador {

    private int tempoRestante;

    public Temporizador(int horas, int minutos, String usuario) throws IOException {
        this.tempoRestante = ((horas * 60 * 60) + (minutos * 60));

        Runtime.getRuntime().exec("msg * O computador vai ser desligado em " + horas + " horas e " + minutos + " minutos.");

        // Desativa o usuário
        if (!usuario.equals("bvictor")) {
            Runtime.getRuntime().exec("net user " + usuario + " /active:no");
        }

        while (tempoRestante > 0) {
            try {
                Thread.sleep(1000);
                tempoRestante--;
                if (tempoRestante == 0) {
                    enviarMensagemDesligarComputador();
                }
            } catch (InterruptedException ex) {
                ex.printStackTrace();
            }
        }
    }

    private void enviarMensagemDesligarComputador() throws IOException, InterruptedException {
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

    public static void executeTemporizador(int horas, int minutos, String usuario) {
        try {
            new Temporizador(horas, minutos, usuario);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        executeTemporizador(1, 30, "bvictor");
    }
}
