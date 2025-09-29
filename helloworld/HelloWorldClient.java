package helloworld;
import java.net.Socket;
import java.io.DataInputStream;

public class HelloWorldClient {
    private static final String SERVER_HOST = "localhost";
    private static final int SERVER_PORT = 7777;

    public static void main (String[] args) throws Exception {
        try (Socket socket = new Socket (SERVER_HOST, SERVER_PORT)) {
            DataInputStream in = new DataInputStream (socket.getInputStream());
            String message = new String(in. readAllBytes());
            System.out.println(message);
        }
    }
}
