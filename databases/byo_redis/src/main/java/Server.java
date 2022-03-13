package com.thundergolfer.uni.byo.redis;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.UUID;

public class Server {
    // TODO(Jonathon): Add EventLoop implementation, like the official Redis uses, instead of threaded.
    private static class ClientHandler extends Thread {
        private Datastore datastore;
        private Socket clientSocket;
        private String clientId;
        private PrintWriter output;
        private BufferedReader input;
        private RedisData.Deserializer deserializer = null;

        public ClientHandler(Datastore store, Socket socket, String clientId)  {
            this.datastore = store;
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
                    if (deserializer == null) {
                        deserializer = new RedisData.Deserializer();
                    }
                    deserializer.process(tokens);
                    if (deserializer.isComplete()) {
                        List<RedisData> data = deserializer.getRedisData();
                        String reply = Commands.runCommand(datastore, data);
                        deserializer.reset();
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
        System.out.printf("Starting Redis-like server on localhost:%d\n", port);
        Datastore store = new Datastore();
        try {
            serverSocket = new ServerSocket(port);
            serverSocket.setReuseAddress(true);
            while (true) {
                uuid = UUID.randomUUID();
                new ClientHandler(
                        store,
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
