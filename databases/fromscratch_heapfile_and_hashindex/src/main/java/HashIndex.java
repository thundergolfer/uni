import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

/**
 * HashIndex will need to map from key -to-> record_id (rid)
 *
 * Currently my HeapFile doesn't have the notion of a record_id, so that will
 * need to be added. Something like page_num + byte_offset would work with my current
 * Heapfile implementation
 */
public class HashIndex {

    private String heapfilePath;
    private String indexFilePath;
    private List<String> heapfileHeader;
    private LinearTable index;
    private int pageSize;
    private int fieldIndex;
    private static String keyValueDelimiter = "|";
    private static String recordValuesDelimiter = ",";

    public HashIndex(String heapfilePath, List<String> heapfileHeader, int pageSize) {
        this.pageSize = pageSize;
        this.heapfileHeader = heapfileHeader;
        this.heapfilePath = heapfilePath;
    }

    public HashIndex(String indexFilePath) {
        this.index = new LinearTable();
        this.indexFilePath = indexFilePath;
    }

    public void create(String fieldName) {
        // find field name index in header
        int index = 0; // TODO: actually implement
        // call with index
        create(index);
    }

    public void create(int fieldIndex) {
        this.fieldIndex = fieldIndex;
        this.index = new LinearTable();

        File f = new File(this.heapfilePath);
        if(!f.exists() || f.isDirectory()) {
            System.err.format("Could not find file '%s' in directory.\n", this.heapfilePath);
            System.exit(1);
        }

        long fileLen = f.length();
        long fileOffset = 0;
        byte[] bytes = new byte[pageSize];
        try {
            RandomAccessFile raf = new RandomAccessFile(this.heapfilePath, "r");

            while (fileOffset <= fileLen) {
                raf.seek(fileOffset);
                raf.read(bytes);

                System.err.format("Indexing new page at offset: %d\n", fileOffset);
                HeapPage.index(index, (int) fileOffset, bytes, dbquery.recordDesc, fieldIndex);

                fileOffset += pageSize;
            }

            raf.close();
        } catch(IOException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
    }

    public void save() throws IOException {
        if (this.index == null) {
            System.err.println("Must call create(int fieldIndex) first");
            return;
        }

        String outfile = constructIndexOutputPath();
        this.index.write(outfile);
        return;
    }

    private String constructIndexOutputPath() {
        StringBuilder builder = new StringBuilder();
        builder.append("hash");
        builder.append(".");
        builder.append(String.valueOf(pageSize));
        return builder.toString();
    }

    public List<String> get(String key) {
        return this.index.retrieve(key);
    }

    public List<String> getFromFile(String key) {
        try {
            return this.index.retrieveFromDisk(key, this.indexFilePath);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }
}
