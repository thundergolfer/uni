import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

public class Main {
    // TODO(Jonathon): Add EventLoop implementation, like the official Redis uses, instead of threaded.
    private static class ClientHandler extends Thread {
        private Socket clientSocket;
        private String clientId;
        private PrintWriter output;
        private BufferedReader input;
        private RedisSerializationProtocol.Array respArr = null;

        public ClientHandler(Socket socket, String clientId)  {
            this.clientSocket = socket;
            this.clientId = clientId;
        }

        @Override
        public void run() {
            try {
                output = new PrintWriter(clientSocket.getOutputStream(), true);
                input = new BufferedReader(
                        new InputStreamReader(clientSocket.getInputStream())
                );
                String clientMsgLine;
                while ((clientMsgLine = input.readLine()) != null) {
                    System.out.printf("Received %s from client %s\n", clientMsgLine, clientId);
                    Scanner scanner = new Scanner(clientMsgLine);
                    List<Token> tokens = scanner.scanTokens();
                    System.out.println(tokens);
                    if (RedisSerializationProtocol.isRESPArray(tokens)) {
                        if (respArr != null) {
                            System.out.println("Woops! Restarted RESP Array.");
                        }
                        int arrSize = Integer.parseInt(tokens.get(1).lexeme);
                        respArr = new RedisSerializationProtocol.Array(arrSize);;
                    } else if (respArr != null) {
                      // In middle of RESP Array building.
                      respArr.addItem(tokens);
                      if (respArr.isFilled()) {
                          System.out.println("Done!");
                          System.out.println(respArr.toString());
                          // RESP Array command
                          String reply = Commands.runCommand(respArr);
                          output.print(reply);
                          output.flush();
                          respArr = null; // Reset RESP Array.
                      }
                    } else {
                        // Simple command
                        String reply = Commands.runCommand(tokens);
                        output.print(reply);
                        output.flush();
                    }
                }
            } catch (CommandException e) {
                System.out.println("Could not run command. " + e.getMessage());
            } catch (ScannerException e) {
                System.out.println("Could not scan client request. " + e.getMessage());
            } catch (IOException e) {
                System.out.println("IOException: " + e.getMessage());
            } finally {
                try {
                    if (clientSocket != null) {
                        clientSocket.close();
                    }
                } catch (IOException e) {
                    System.out.println("IOException: " + e.getMessage());
                }
            }
        }
    }

    public static void main(String[] args) {
        ServerSocket serverSocket;
        UUID uuid;
        int port = 6379;

        // You can use print statements as follows for debugging, they'll be visible when running tests.
        System.out.printf("Starting Redis-like server on localhost:%d\n", port);
        try {
            serverSocket = new ServerSocket(port);
            serverSocket.setReuseAddress(true);
            while (true) {
                uuid = UUID.randomUUID();
                new ClientHandler(
                        serverSocket.accept(),
                        uuid.toString()
                ).start();
            }
        } catch (IOException e) {
            System.out.println("IOException: " + e.getMessage());
            System.exit(1);
        }
    }
}
