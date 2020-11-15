package server;

import java.io.*;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

import com.sun.net.httpserver.HttpServer;

public class Server {
    /**
     * This very basic HTTP Server receives from the `technical_documentation_website` starlark rule's
     * implementation a number of Markdown documents preprocessed by `technical_documents` rules (and included in
     * runfiles).
     *
     * For example:
     *
     * <pre>
     *   technical_documents(
     *      name = "readmes",
     *      inputs = ["README.md", "CONTRIBUTING.md"],
     *   )
     *
     *   technical_documentation_website(
     *      name = "demo_docs_website",
     *      srcs = {
     *          "//:readmes": "/foo"  # <key = document> : <value = position in website's doc-tree>
     *      }
     *  )
     * </pre>
     *
     * Makes the docs in <pre>:readmes</pre> available at "/foo/README.md" and "/foo/CONTRIBUTING.md", respectively.
     * "/foo/README" and "/foo/CONTRIBUTING" would also be valid.
     */
    public static void main(String[] args) throws Exception {
        Map<String, String> routeToDocFile = processArgs(args);
        int portNumber = 8000;

        System.out.printf("🚀 Starting web server at localhost:%s\n", portNumber);
        HttpServer server = HttpServer.create(new InetSocketAddress(portNumber), 0);
        server.createContext("/", new BaseHandler(routeToDocFile));
        server.setExecutor(null); // creates a default executor
        server.start();
    }

    /**
     * The Server expects to receive as argument only a series of pairs of strings,
     * in the form:
     * <url sub-path> <runfiles path to .md doc> <url sub-path> <runfiles path to .md doc> ...
     *
     * This list of arguments is broken up into a route map for the HttpHandler.
     *
     * @param args
     * @return A Map from path route -> runfiles location of a markdown document.
     */
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
