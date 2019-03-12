package PayloadServerClient;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class MyServer {
    private static ServerSocket server;
    private static Socket socket;
    private static BufferedReader br;
    private static ObjectOutputStream clientOutputStream;
    private static ObjectInputStream clientInputStream;

    private MyServer(int port) {
        System.out.println("Starting server...");
        try {
            server = new ServerSocket(port);
            System.out.println("Waiting for Client...");

            socket = server.accept();   // Waits till the client connects.
            System.out.println("Client connected: " + socket.getLocalAddress());

            br = new BufferedReader(new InputStreamReader(System.in));  // To read from keyboard
            clientOutputStream = new ObjectOutputStream(socket.getOutputStream());  // To write into Socket
            clientInputStream = new ObjectInputStream(socket.getInputStream()); // To read from socket

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) throws IOException {
        new MyServer(3000);
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
