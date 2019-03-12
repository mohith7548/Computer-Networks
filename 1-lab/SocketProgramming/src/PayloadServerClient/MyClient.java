package PayloadServerClient;

import java.io.*;
import java.net.Socket;

public class MyClient {
    private static Socket socket;
    private static BufferedReader br;
    private static ObjectOutputStream clientOutputStream;
    private static ObjectInputStream clientInputStream;

    private MyClient(String ip, int port) {
        try {
            System.out.println("Trying to connect....");
            socket = new Socket(ip, port);
            System.out.println("Connected to Server.");

            br = new BufferedReader(new InputStreamReader(System.in));  // To read from keyboard
            clientOutputStream = new ObjectOutputStream(socket.getOutputStream());  // To write into Socket
            clientInputStream = new ObjectInputStream(socket.getInputStream()); // To read from socket


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        new MyClient("localhost", 3000);
        String wBuffer;
        // This listener keeps listening for the messages in the socket and prints them.
        new Thread(new Listener(clientInputStream)).start();
        System.out.println("Good to go now. Type your message and hit return.");
        while (true) {
            if(!(wBuffer = br.readLine()).equals("")) {
                Payload payload = new Payload(socket.getLocalAddress().toString(), wBuffer);
                clientOutputStream.writeObject(payload);
            }
        }
    }
}

