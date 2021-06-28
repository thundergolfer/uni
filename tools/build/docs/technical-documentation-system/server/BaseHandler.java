package server;

import java.io.*;
import java.util.Map;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import com.google.devtools.build.runfiles.Runfiles;

@SuppressWarnings("restriction")
public class BaseHandler implements HttpHandler {
    Map<String, String> routeToStaticFile;
    final String DEFAULT_INDEX_PAGE_LOCATION = "uni/tools/build/docs/technical-documentation-system/server/static/index.html";
    final String DEFAULT_404_PAGE_LOCATION = "uni/tools/build/docs/technical-documentation-system/server/static/404.html";

    public BaseHandler(Map<String, String> routeToStaticFile) {
        this.routeToStaticFile = routeToStaticFile;
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        Runfiles runfiles = Runfiles.create();
        Headers headers = exchange.getResponseHeaders();
        String fileId = exchange.getRequestURI().getPath();
        String key = fileId;

        if (key.equals("/")) {
            // TODO(Jonathon): How do users specify the index page to replace the default? It can't just be a technical_documents target because they contain many docs.
            System.out.println("No Index page registered. Falling back to thundergolfer/technical_document_system Index page.");
            handleIndex(exchange, runfiles);
            return;
        }

        System.out.printf("Retrieving '%s'\n", key);
        String docFilepath = this.routeToStaticFile.getOrDefault(key, key);
        File file = getFile(runfiles, docFilepath);
        if (file == null) {
            handle404(exchange, runfiles);
        } else {
            String line;
            StringBuilder resp = new StringBuilder();

            try {
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
                while ((line = bufferedReader.readLine()) != null) {
                    resp.append(line);
                    resp.append("\n");
                }
                bufferedReader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }

            String markdownResp = MarkdownRenderer.render(resp.toString());

            headers.add("Content-Type", "text/html");
            exchange.sendResponseHeaders(200, markdownResp.length());
            OutputStream outputStream = exchange.getResponseBody();
            outputStream.write(markdownResp.getBytes());
            outputStream.close();
        }
    }

    public void handleIndex(HttpExchange exchange, Runfiles runfiles) throws IOException {
        Headers headers = exchange.getResponseHeaders();
        String line;
        String resp = "";
        try {
            String indexFilepath = runfiles.rlocation(DEFAULT_INDEX_PAGE_LOCATION);
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

    public void handle404(HttpExchange exchange, Runfiles runfiles) throws IOException {
        Headers headers = exchange.getResponseHeaders();
        String line;
        String resp = "";
        try {
            String indexFilepath = runfiles.rlocation(DEFAULT_404_PAGE_LOCATION);
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
        exchange.sendResponseHeaders(404, resp.length());
        OutputStream outputStream = exchange.getResponseBody();
        outputStream.write(resp.getBytes());
        outputStream.close();
    }

    private File getFile(Runfiles runfiles, String fileId) {
        String path = runfiles.rlocation(fileId);
        if (path == null) {
            return null;
        }
        File f = new File(path);
        if (f.exists() && f.isFile()) {
            return f;
        }
        return null;
    }
}
