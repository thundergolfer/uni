package preprocessor;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
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

        Set<String> referenceFiles = new HashSet(
                Arrays.asList(Arrays.copyOfRange(args, 2, args.length))
        );

        if (!mdFile.exists()) {
            throw new IllegalArgumentException("Must pass markdown file that exists.");
        }

        String markdownFileContents = readMarkdownFile(mdFile);

        String processedMarkdownFileContents;
        try (PrintWriter out = new PrintWriter(writeFile)) {
            processedMarkdownFileContents = processReferences(markdownFileContents, referenceFiles);
            System.out.println(processedMarkdownFileContents);
            out.println(processedMarkdownFileContents);
        } catch (ReferenceProcessingException e) {
            e.printStackTrace();
            System.exit(1);
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

    private static String processReferences(String mdContents, Set<String> referenceFiles) throws ReferenceProcessingException, IOException {
        Pattern p = Pattern.compile("%% .+ %%", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(mdContents);
        String matchedRef;
        StringBuffer sb = new StringBuffer();
        while(m.find()) {
            matchedRef = m.group(0);
            matchedRef = removePrefix(matchedRef, "%% ");
            matchedRef = removeSuffix(matchedRef, " %%");
            Substitution sub = parseSubstitution(matchedRef);
            if (!referenceFiles.contains(sub.filePath)) {
                String errMsg = String.format(
                        "Invalid file reference. '%s' not found. A relevant target be missing from the 'references' attribute.",
                        sub.filePath
                );
                throw new ReferenceProcessingException(errMsg);
            }
            String requestedSubstitutionContents = extractSubstitutionContents(sub);
            System.out.println("requested substitution");
            System.out.println(requestedSubstitutionContents);
            m.appendReplacement(sb, requestedSubstitutionContents);
        }
        m.appendTail(sb);
        return sb.toString();
    }

    private static String extractSubstitutionContents(Substitution sub) throws IOException {
        List<String> requestedLines;
        Path p = new File(sub.filePath).toPath();
        List<String> fileLines = Files.readAllLines(p);

        if (sub.lineStart.isPresent() && sub.lineEnd.isPresent()) {
            int lineStart = sub.lineStart.get();
            int lineEnd = sub.lineEnd.get();
            if (lineStart > lineEnd) {
                requestedLines = new ArrayList<>();
            } else if (lineStart == lineEnd) {
                requestedLines = new ArrayList<>();
                requestedLines.add(fileLines.get(lineStart-1));
            } else {
                int safeLineEnd = Math.min(lineEnd, fileLines.size());
                requestedLines = fileLines.subList(lineStart-1, safeLineEnd);
            }
        } else {
            requestedLines = fileLines;
        }
        return String.join("\n", requestedLines);
    }

    // VisibleForTesting
    protected static Substitution parseSubstitution(String substitutionDirective) throws ReferenceProcessingException {
        String[] parts = substitutionDirective.split("\\s+");
        switch (parts.length) {
            case 1:
                return new Substitution(parts[0]);
            case 2:
                String lineRangeDeclaration = parts[1];
                String[] lineRangeDeclarationParts = lineRangeDeclaration.split("-");
                if (lineRangeDeclarationParts.length != 2) {
                    throw new ReferenceProcessingException("Wrong line range declaration fmt. Valid format example: 1-19");
                }
                try {
                    int lineStart = Integer.parseInt(lineRangeDeclarationParts[0]);
                    int lineEnd = Integer.parseInt(lineRangeDeclarationParts[1]);
                    return new Substitution(parts[0], lineStart, lineEnd);
                } catch (NumberFormatException e) {
                    throw new ReferenceProcessingException("Could not parse integer in line range declaration. Valid format example: 1-19");
                }
            default:
                throw new ReferenceProcessingException("Fuck");
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

    protected static class Substitution {
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
}
