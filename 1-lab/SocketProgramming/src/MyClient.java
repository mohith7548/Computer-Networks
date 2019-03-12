import java.io.*;
import java.net.Socket;

public class MyClient {
    private static Socket socket;
    private static BufferedReader br;
    private static BufferedReader socketReader;
    private static PrintWriter socketWriter;

    private MyClient(String ip, int port) {
        try {
            System.out.println("Trying to connect....");
            socket = new Socket(ip, port);
            System.out.println("Connected to Server.");

            br = new BufferedReader(new InputStreamReader(System.in));  // To read from keyboard
            socketReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));  // To read from socket
            socketWriter = new PrintWriter(socket.getOutputStream(), true); // To write into Socket


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException {
        new MyClient("localhost", 3000);
        String wBuffer;
        // This listener keeps listening for the messages in the socket and prints them.
        new Thread(new Listener(socketReader, ">")).start();
        System.out.println("Good to go now. Type your message and hit return.");
        while (true) {
//            System.out.println("client: ");
            if(!(wBuffer = br.readLine()).equals("")) {
                socketWriter.println(wBuffer);
                socketWriter.flush();
            }
        }
    }
}

