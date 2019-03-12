import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class MyServer {
    private static ServerSocket server;
    private static Socket socket;
    private static BufferedReader br;
    private static BufferedReader socketReader;
    private static PrintWriter socketWriter;

    private MyServer(int port) {
        System.out.println("Starting server...");
        try {
            server = new ServerSocket(port);
            System.out.println("Waiting for Client...");

            socket = server.accept();   // Waits till the client connects.
            System.out.println("Client connected: " + socket.getLocalAddress());

            br = new BufferedReader(new InputStreamReader(System.in));  // To read from keyboard
            socketReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));  // To read from socket
            socketWriter = new PrintWriter(socket.getOutputStream(), true); // To write into Socket

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) throws IOException {
        new MyServer(3000);
        String wBuffer;
        // This listener keeps listening for the messages in the socket and prints them.
        new Thread(new Listener(socketReader, ">")).start();
        System.out.println("Good to go now. Type your message and hit return.");
        while (true) {
//            System.out.println("server: ");
            if(!(wBuffer = br.readLine()).equals("")) {
                socketWriter.println(wBuffer);
                socketWriter.flush();
            }
        }
    }
}
