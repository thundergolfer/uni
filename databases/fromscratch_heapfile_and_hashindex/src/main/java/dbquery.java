import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.file.Path;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;

public class dbquery {
    private static final String usageMsg = "USAGE: java dbquery <QUERY TEXT> <HEAP FILE> [--index <INDEX FILE>] [--exact-match]";
    private static int pageSize;
    private static long executionTimeInMilliseconds;

    protected final static TupleDesc<String> recordDesc = new TupleDesc() {{
        add("TEXT"); // (Irrelevant)
        add("TEXT"); // Business Name (BN_NAME)
        add("TEXT"); // Status
        add("TEXT"); // Date of Registration
        add("TEXT"); // Date of Cancellation
        add("TEXT"); // Renewal Date
        add("TEXT"); // Former State Number
        add("TEXT"); // Previous State of Registration
        add("LONG"); // Australian Business Number (ABN)
    }};
    private static int colToSearch = 1;

    public static void main(String[] args) {
        final long startTime = System.nanoTime();
        boolean doExactMatch = false;
        boolean useIndex = false;
        if (args.length < 2) {
            System.err.println(usageMsg);
            System.exit(1);
        }

        String queryText = args[0];

        try {
            pageSize = Integer.parseInt(args[1]);
        } catch(NumberFormatException e) {
            System.err.println("Must provide a valid integer page size. eg. 2048");
            System.exit(1);
        }
        String datafilePath = PathUtils.constructHeapfilePath(pageSize);

        HashIndex hashIndex = null;
        if (args.length >= 4) {
            if (args[2].equals("--index ")) {
                System.err.println(usageMsg);
                System.exit(1);
            }

            String indexFilePath = args[3];
            hashIndex = new HashIndex(indexFilePath);
            useIndex = true;
        }

        if (args.length == 5 && args[4].equals("--exact-match")) {
            System.err.println("Using exact-match query");
            doExactMatch = true;
        }

        File f = new File(datafilePath);
        if(!f.exists() || f.isDirectory()) {
            System.err.format("Could not find heap file '%s' in directory.\n", datafilePath);
            System.exit(1);
        }

        if (useIndex && hashIndex != null) {
            HeapFile heapFile = new HeapFile(pageSize, datafilePath);
            indexedSearch(heapFile, hashIndex, datafilePath, queryText, doExactMatch);
        } else {
            sequentialSearch(f, datafilePath, queryText);
        }

        final long duration = System.nanoTime() - startTime;
        executionTimeInMilliseconds = TimeUnit.NANOSECONDS.toMillis(duration);

        System.out.format(
                "Execution Time (ms): %s\n",
                executionTimeInMilliseconds
        );

        System.exit(0);
    }

    public static void indexedSearch(HeapFile heapfile, HashIndex index, String datafilePath, String queryText, boolean exactMatch) {
        queryText = queryText.toLowerCase();
        List<String> res = index.getFromFile(queryText);

        if (res != null) {
            for (String strLoc : res) {
                int recordLoc = Integer.valueOf(strLoc);
                Tuple t = heapfile.readRecord(recordLoc);
                System.out.println(t.toString());
            }
        }
    }

    public static void sequentialSearch(File f, String datafilePath, String queryText) {
        long fileLen = f.length();
        long offset = 0;
        byte[] bytes = new byte[pageSize];
        try {
            RandomAccessFile raf = new RandomAccessFile(datafilePath, "r");

            while (offset <= fileLen) {
                raf.seek(offset);
                raf.read(bytes);

                System.err.format("Searching new page at offset: %d\n", offset);
                HeapPage.searchInHeapPage(queryText, bytes, recordDesc, colToSearch);

                offset += pageSize;
            }
            raf.close();
        } catch(IOException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
    }
}
