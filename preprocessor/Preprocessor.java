package preprocessor;

import java.io.*;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * USAGE: Preprocessor.jar <input file> <output file> [<references> ...]
 */
public class Preprocessor {

    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            throw new IllegalArgumentException("Incorrect arguments passed to program.");
        }

        String markdownFilePath = args[0];
        File mdFile = new File(markdownFilePath);
        String writeFilePath = args[1];
        File writeFile = new File(writeFilePath);

        String[] reference_files = Arrays.copyOfRange(args, 2, args.length);
        for (String ref: reference_files) {
            System.out.printf("REF: %s\n", ref);
        }

        if (!mdFile.exists()) {
            throw new IllegalArgumentException("Must pass markdown file that exists.");
        }

        String markdownFileContents = readMarkdownFile(mdFile);
        System.out.println(markdownFileContents);

        String processedMarkdownFileContents = processReferences(markdownFileContents);

        System.out.println(processedMarkdownFileContents);

        try (PrintWriter out = new PrintWriter(writeFile)) {
            out.println(markdownFileContents);
        }
    }

    private static String readMarkdownFile(File mdFile) throws IOException {
        try(BufferedReader br = new BufferedReader(new FileReader(mdFile))) {
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();

            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();
            }
            return sb.toString();
        }
    }

    private static String processReferences(String mdContents) {
        Pattern p = Pattern.compile("%% \\/\\/[0-9a-z_-]+:[0-9a-z_-]+ %%", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(mdContents);
        String result = m.replaceAll("FOOBAR, My son!");

        return result;
    }
}
