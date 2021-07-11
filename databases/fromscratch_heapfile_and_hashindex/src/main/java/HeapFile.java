import java.io.*;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class HeapFile {
    private int pageSize;
    private int numPagesWritten;
    private long bytesWritten;
    private String outfile;
    private byte delimiter;
    private HeapPage currentPage;

    private double BytesInMB = 1000000;

    HeapFile(int pageSize, String outfilePath) {
        this.pageSize = pageSize;
        this.outfile = outfilePath;
        this.numPagesWritten = 0;
        this.delimiter = (byte) '|';
        this.currentPage = new HeapPage(this.pageSize);
    }

    public void clearData() {
        // Truncate the file in-case it's not empty
        try {
            FileWriter f = new FileWriter(this.outfile);
            f.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean addRecord(Tuple t) {
        // check if record will fit in current page
        if (t.length() <= currentPage.bytesLeft()) {
            currentPage.addRecord(t);
            return true;
        } else {
            try {
                writeCurrentPage();
            } catch(IOException e) {
                System.err.println(e.getMessage());
                return false;
            }

        }

        return true;
    }

    public Tuple readRecord(int offset) {
        int page = offset / pageSize;
        int pageOffset = offset % pageSize;
        System.err.format("Reading record from page %d at page offset %d\n", page, pageOffset);

        File f = new File(outfile);
        if(!f.exists() || f.isDirectory()) {
            System.err.format("Could not find file '%s' in directory.\n", outfile);
            System.exit(1);
        }

        try {
            RandomAccessFile raf = new RandomAccessFile(outfile, "r");
            raf.seek(page * pageSize);
            byte[] data = new byte[pageSize];
            raf.read(data);

            int start = pageOffset;
            int end = pageOffset;
            int currCol = 0;
            Item currItem;
            int numCols = dbquery.recordDesc.size();
            byte delimiter = (byte)'|';

            Item[] items = new Item[numCols];

            while (start < data.length) {
                while (end < data.length && data[end] != delimiter) {
                    end++; // won't go out of bound because all pages end with '|'
                }

                byte[] itemBytes = Arrays.copyOfRange(data, start, end);

                String type = (String) dbquery.recordDesc.get(currCol);
                switch (type) {
                    case "TEXT":
                        String val = new String(itemBytes);
                        currItem = new StringItem(val);
                        break;
                    case "LONG":
                        if (itemBytes.length != Long.BYTES) {
                            currItem = null;
                            break;
                        }
                        long longVal = ByteUtils.bytesToLong(itemBytes);
                        currItem = new LongItem(longVal);
                        break;
                    default:
                        System.err.format("Found unrecognised item type: %s", type);
                        return null;
                }
                items[currCol] = currItem;
                currCol = (currCol + 1) % numCols; // go to next

                if (currCol == 0) { // a full tuple has been completed
                    return new Tuple(items);
                }
                start = end + 1;
                end = end + 1;
            }
            raf.close();
        } catch(IOException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }

        return null;
    }

    public void flush() throws IOException {
        if (!this.currentPage.empty()) {
            writeCurrentPage();
        }
    }

    public int getNumPagesWritten() {
        return numPagesWritten;
    }

    private void writeCurrentPage() throws IOException {
        System.err.format("Writing current Heap Page to '%s'. MB written: %f\n", this.outfile, (double) this.bytesWritten / this.BytesInMB);
        FileOutputStream fileOut = new FileOutputStream(this.outfile, true);
        DataOutputStream os = new DataOutputStream(fileOut);

        currentPage.write(os, this.delimiter);
        currentPage = new HeapPage(this.pageSize);

        os.flush();
        os.close();
        numPagesWritten++;
        bytesWritten += this.pageSize;
    }
}
