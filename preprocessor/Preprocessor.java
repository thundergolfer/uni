package preprocessor;

import java.io.*;
import java.util.Arrays;
import java.util.Optional;
import java.util.regex.MatchResult;
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
        Pattern p = Pattern.compile("%% .+ %%", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(mdContents);
        String matchedRef;
        while(m.find()) {
            System.out.println(m.group(0));
            matchedRef = m.group(0);
            matchedRef = removePrefix(matchedRef, "%% ");
            System.out.println(matchedRef);
            matchedRef = removeSuffix(matchedRef, " %%");
            Substitution sub = parseSubstitution(matchedRef);
            System.out.println(sub);
        }
        return m.replaceAll("FOOBAR, My son!");
    }

    private static Substitution parseSubstitution(String substitutionDirective) {
        String[] parts = substitutionDirective.split("\\s+");
        System.out.println(substitutionDirective);
        switch (parts.length) {
            case 1:
                return new Substitution(parts[0]);
            case 2:
                return new Substitution(parts[1]);
            default:
                throw new RuntimeException("Fuck");
        }
    }

    private static class Substitution {
        String filePath;
        Optional<Integer> lineStart;
        Optional<Integer> lineEnd;

        public Substitution(String filePath) {
            this.filePath = filePath;
            lineStart = Optional.empty();
            lineEnd = Optional.empty();
        }

        public Substitution(String filePath, int lineStart, int lineEnd) {
            this.filePath = filePath;
            this.lineStart = Optional.of(lineStart);
            this.lineEnd = Optional.of(lineEnd);
        }

        public String toString() {
            return filePath + " " + lineStart.toString() + "-" + lineEnd.toString();
        }
    }

    private static String removePrefix(String s, String prefix) {
        if (s != null && prefix != null && s.startsWith(prefix)){
            return s.substring(prefix.length());
        }
        return s;
    }

    private static String removeSuffix(String s, String suffix) {
        if (s != null && suffix != null && s.endsWith(suffix)){
            return s.substring(0, s.length() - suffix.length());
        }
        return s;
    }
}
