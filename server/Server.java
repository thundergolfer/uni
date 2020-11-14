package server;

import java.io.*;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import com.google.devtools.build.runfiles.Runfiles;

public class Server {
    public static void main(String[] args) throws Exception {
        Map<String, String> routeToDocFile = processArgs(args);

        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new IndexPageHandler());
        server.createContext("/test", new MyHandler());
        server.createContext("/static", new StaticFileHandler(routeToDocFile));
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
                System.out.println("Name of file: " + newFile.getName());
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(new FileInputStream(newFile)));
                while ((line = bufferedReader.readLine()) != null) {
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

    private static Map<String, String> processArgs(String[] args) {
        if (args.length % 2 != 0) throw new IllegalArgumentException();
        String [][] pairs = chunkArrayIntoPairs(args);
        return pairsIntoMap(pairs);
    }

    private static String[][] chunkArrayIntoPairs(String[] array) {
        int numPerChunk = 2;
        int numOfChunks = (int)Math.ceil((double)array.length / numPerChunk);
        String[][] output = new String[numOfChunks][];

        for(int i = 0; i < numOfChunks; ++i) {
            int start = i * numPerChunk;
            int length = Math.min(array.length - start, numPerChunk);
            String[] temp = new String[length];
            System.arraycopy(array, start, temp, 0, length);
            output[i] = temp;
        }
        return output;
    }

    private static Map<String, String> pairsIntoMap(String[][] pairs) {
        Map<String, String> m = new HashMap<>();
        for (String[] pair: pairs) {
            if (pair.length != 2) throw new AssertionError("Function only accepts an array of pairs (len=2 array)");
            m.put(pair[0], pair[1]);
        }
        return m;
    }
}
