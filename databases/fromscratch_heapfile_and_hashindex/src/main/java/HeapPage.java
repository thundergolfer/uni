import java.io.DataOutputStream;
import java.io.IOException;
import java.util.*;

public class HeapPage {
    private int pageSize;
    private int currBytesUsed;
    private List<Tuple> tuples;

    public HeapPage(int pageSize) {
        this.pageSize = pageSize;
        this.currBytesUsed = 0;
        this.tuples = new ArrayList<>();
    }

    public static void index(LinearTable index, int offset, byte[] data, TupleDesc recordDesc, int indexColumn) {
        int start = 0;
        int end = 0;
        int currCol = 0;
        int recordStart = 0;
        Item currItem;
        int numCols = recordDesc.size();
        byte delimiter = (byte)'|';

        Item[] items = new Item[numCols];

        while (start < data.length) {
            while (end < data.length && data[end] != delimiter) {
                end++; // won't go out of bound because all pages end with '|'
            }

            if (end == data.length && data[end-1] != delimiter) {
                return; // at end of file and byte is not valid field end
            }

            byte[] itemBytes = Arrays.copyOfRange(data, start, end);

            String type = (String) recordDesc.get(currCol);
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
                    return;
            }
            items[currCol] = currItem;
            currCol = (currCol + 1) % numCols; // go to next

            if (currCol == 0) { // a full tuple has been completed
                Tuple t = new Tuple(items);
                String fieldToIndex = t.getItem(indexColumn).toString();

//                Set<Integer> locations = index.get(fieldToIndex);
//                if (locations == null) {
//                    locations = new HashSet<>();
//                }
                //                locations.add(recordStart);
                fieldToIndex = fieldToIndex.toLowerCase();
                int absoluteRecordStart = recordStart + offset;
                System.err.format("Adding '%s' at %d\n", fieldToIndex, absoluteRecordStart);
                index.add(fieldToIndex, String.valueOf(absoluteRecordStart));

                if (data[end] == (byte)0) {
                    // reaching end of page padding
                    return;
                }
                recordStart = end + 1;
                System.err.format("new record starts at: %d\n", recordStart);
            }
            start = end + 1;
            end = end + 1;
        }
        return;
    }

    public static void searchInHeapPage(String query, byte[] data, TupleDesc recordDesc, int searchColumn) {
        int start = 0;
        int end = 0;
        int currCol = 0;
        Item currItem;
        int numCols = recordDesc.size();
        byte delimiter = (byte)'|';

        Item[] items = new Item[numCols];

        query = query.toLowerCase(); // case invariant search

        while (start < data.length) {
            while (end < data.length && data[end] != delimiter) {
                end++; // won't go out of bounds because all pages end with '|'
            }

            if (end == data.length && data[end-1] != delimiter) {
                return; // at end of file and byte is not valid field end
            }

            byte[] itemBytes = Arrays.copyOfRange(data, start, end);

            String type = (String) recordDesc.get(currCol);
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
                    return;
            }
            items[currCol] = currItem;
            currCol = (currCol + 1) % numCols; // go to next

            if (currCol == 0) { // a full tuple has been completed
                Tuple t = new Tuple(items);
                String fieldToSearch = t.getItem(searchColumn).toString();
                if (fieldToSearch.toLowerCase().contains(query)) {
                    System.out.println(t.toString());
                }

                if (data[end] == (byte)0) {
                    // reaching end of page padding
                    return;
                }
            }
            start = end + 1;
            end = end + 1;
        }

    }

    public int bytesLeft() {
        return pageSize - currBytesUsed;
    }

    public boolean empty() {
        return currBytesUsed == 0;
    }

    public void addRecord(Tuple t) {
        this.currBytesUsed += t.length();
        this.tuples.add(t);
    }

    public void write(DataOutputStream os, byte delimiter) throws IOException {
        for (Tuple t : tuples) {
            for (Item i : t.getItems()) {
                if (i != null) {
                    i.serialize(os);
                }
                os.write(delimiter);
            }
        }

        // write the padding to 4096
        byte[] padding = new byte[bytesLeft()];
        for (int i = 0; i < bytesLeft(); i++) {
            padding[0] = (byte)'\0';
        }
        os.write(padding);
    }
}
