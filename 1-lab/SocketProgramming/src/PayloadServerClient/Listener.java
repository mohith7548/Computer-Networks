package PayloadServerClient;
import java.io.ObjectInputStream;

class Listener extends Thread {
    private static ObjectInputStream socketReader;

    public Listener(ObjectInputStream socketReader) {
        this.socketReader = socketReader;
    }

    public void run() {
        try {
            Payload payload;
            while ((payload = (Payload) socketReader.readObject()) != null) {
                System.out.println(payload.toString());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        Listener obj = new Listener(socketReader);
        obj.start();
    }
}