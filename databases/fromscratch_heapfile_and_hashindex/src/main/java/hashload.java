import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class hashload {
    private final static String usageMsg = "USAGE: java hashload <PAGE SIZE>";


    private final static List<String> header = new LinkedList<>(Arrays.asList(
            "REGISTER_NAME",
            "BN_NAME",
            "BN_STATUS",
            "BN_REG_DT",
            "BN_CANCEL_DT",
            "BN_RENEW_DT",
            "BN_STATE_NUM",
            "BN_STATE_OF_REG",
            "BN_ABN"
    ));

    private static int parseHeapfilePath(String[] args) {
        if (args.length < 1) {
            return -1;
        }
        return Integer.valueOf(args[0]);
    }

    private static String parseIndexField(String[] args) {
        if (args.length < 2) {
            return null;
        }
        return args[1];
    }

    private static int getPagesizeFromHeapfilePath(String heapfilePath) {
        String extension = "";
        int i = heapfilePath.lastIndexOf('.');
        if (i > 0) {
            extension = heapfilePath.substring(i+1);
        }
        int pagesize = Integer.valueOf(extension);

        return pagesize;
    }

    public static void main(String[] args) throws IOException  {
        int pageSize = parseHeapfilePath(args);
        String heapfilePath = "heap." + String.valueOf(pageSize);
        String field = "BN_NAME";

        if (pageSize < 0 || field == null) {
            System.err.println(usageMsg);
            System.exit(1);
        }

        int fieldIndex = header.indexOf(field);
        if (fieldIndex < 0) {
            System.err.format("%s is not a valid field for indexing\n", field);
            System.exit(0);
        }
        System.err.format("Index of key field: %d  Name of key field: %s\n", fieldIndex, field);

        HashIndex hf = new HashIndex(
                heapfilePath,
                header,
                pageSize
        );

        hf.create(fieldIndex);
        hf.save();
    }
}
