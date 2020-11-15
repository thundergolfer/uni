package server;

import java.io.*;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

import com.sun.net.httpserver.HttpServer;

public class Server {
    public static void main(String[] args) throws Exception {
        Map<String, String> routeToDocFile = processArgs(args);
        int portNumber = 8000;

        System.out.printf("🚀 Starting web server at localhost:%s\n", portNumber);
        HttpServer server = HttpServer.create(new InetSocketAddress(portNumber), 0);
        server.createContext("/", new BaseHandler(routeToDocFile));
        server.setExecutor(null); // creates a default executor
        server.start();
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
