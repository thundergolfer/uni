package server;

import java.io.*;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import com.google.devtools.build.runfiles.Runfiles;

@SuppressWarnings("restriction")
public class StaticFileHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        Runfiles runfiles = Runfiles.create();
        Headers headers = exchange.getResponseHeaders();
        String fileId = exchange.getRequestURI().getPath();
        System.out.printf("Retrieving %s\n", fileId);
        File file = getFile(runfiles, fileId);
        if (file == null) {
            String response = "Error 404 File not found.";
            exchange.sendResponseHeaders(404, response.length());
            OutputStream output = exchange.getResponseBody();
            output.write(response.getBytes());
            output.flush();
            output.close();
        } else {
            String line;
            String resp = "";

            try {
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
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

    private File getFile(Runfiles runfiles, String fileId) {
        if (fileId.equals("/static/foo")) {
            System.out.printf("No file at %s\n", fileId);
            return null;
        }
        String path = runfiles.rlocation("technical_documentation_system/server/static/test_doc.md");
        return new File(path);
    }
}
