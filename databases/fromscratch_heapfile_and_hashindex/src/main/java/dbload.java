import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;


public class dbload {

    private final static String usageMsg = "USAGE: java dbload -p <PAGESIZE> <DATAFILE>";
    private final static int NUM_FIELDS_IN_DATASET = 9;

    private static HeapFile heapfile;

    private final static TupleDesc<String> recordDesc = new TupleDesc() {{
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

    private static int parsePageSize(String[] args) {
        if (args.length < 2 || !args[0].equals("-p")) {
            return -1;
        }

        try {
            return Integer.parseInt(args[1]);
        } catch(NumberFormatException e) {
            System.err.println("Page size argument must be an integer value. eg: 2048");
            return -1;
        }
    }

    private static String parseDatafilePath(String[] args) {
        if (args.length < 3) {
            return null;
        }
        return args[2];
    }

    private static String[] parseLine(String line) {
        String[] tokens = line.split("\t");

        return tokens;
    }

    public static void main(String[] args) {
        final long startTime = System.nanoTime();

        int numRecordsLoaded = 0;
        int numPagesUsed = 0;
        long executionTimeInMilliseconds = 0;

        int pageSize = parsePageSize(args);
        String datafilePath = parseDatafilePath(args);
        String outputPath = PathUtils.constructHeapfilePath(pageSize);

        Scanner scanner;

        if (pageSize < 0 || datafilePath == null) {
            System.err.println(usageMsg);
            System.exit(1);
        }

        System.err.format("Using pages size: %d (bytes)\n", pageSize);
        heapfile = new HeapFile(pageSize, outputPath);
        heapfile.clearData();

        boolean addRecordSuccess;

        String[] line;
        Tuple t;
        try {
            scanner = new Scanner(new File(datafilePath));

            scanner.nextLine(); // skip the header of the dataset

            while (scanner.hasNext()) {
                line = parseLine(scanner.nextLine());
                t = new Tuple(line, recordDesc);
                addRecordSuccess = heapfile.addRecord(t);
                if (!addRecordSuccess) {
                    System.err.println("Failed to add record to heap file");
                    System.exit(1);
                }

                numRecordsLoaded++;
            }
            scanner.close();
            heapfile.flush(); // write the final page
        } catch(FileNotFoundException e) {
            System.err.format("Valid datafile not found at '%s'", datafilePath);
            System.exit(1);
        } catch(IOException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }

        final long duration = System.nanoTime() - startTime;
        executionTimeInMilliseconds = TimeUnit.NANOSECONDS.toMillis(duration);
        numPagesUsed = heapfile.getNumPagesWritten();

        System.out.format(
                "Number of records loaded: %d\nNumber of pages used: %d\nExecution Time (ms): %d\n",
                numRecordsLoaded,
                numPagesUsed,
                executionTimeInMilliseconds
        );
    }
}
