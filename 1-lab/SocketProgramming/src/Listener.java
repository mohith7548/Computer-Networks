import java.io.BufferedReader;

class Listener extends Thread {
    private static BufferedReader socketReader;
    private static String type;

    public Listener(BufferedReader socketReader, String type) {
        this.socketReader = socketReader;
        this.type = type;
    }

    public void run() {
        try {
            String rBuffer;
            while ((rBuffer = socketReader.readLine()) != null) {
                System.out.println(type + ": " + rBuffer);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String args[]) {
        Listener obj = new Listener(socketReader, type);
        obj.start();
    }
}