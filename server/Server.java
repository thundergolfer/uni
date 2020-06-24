package server;

import java.io.*;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import com.google.devtools.build.runfiles.Runfiles;

public class Server {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new IndexPageHandler());
        server.createContext("/test", new MyHandler());
        server.createContext("/static", new StaticFileHandler());
        server.setExecutor(null); // creates a default executor
        server.start();
    }

    static class IndexPageHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            Runfiles runfiles = Runfiles.create();
            Headers headers = exchange.getResponseHeaders();

            String line;
            String resp = "";
            try {
                String indexFilepath = runfiles.rlocation("technical_documentation_system/server/static/index.html");
                File newFile = new File(indexFilepath);
                System.out.println("*****lecture du fichier*****");
                System.out.println("nom du fichier: " + newFile.getName());
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(new FileInputStream(newFile)));
                while ((line = bufferedReader.readLine()) != null) {
                    System.out.println(line);
                    resp += line;
                }
                bufferedReader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }

            headers.add("Content-Type", "text/html");
            exchange.sendResponseHeaders(200, resp.length());
            OutputStream outputStream = exchange.getResponseBody();
            outputStream.write(resp.getBytes());
            outputStream.close();
        }
    }

    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange t) throws IOException {
            String response = "This is the response";
            t.sendResponseHeaders(200, response.length());
            OutputStream os = t.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
