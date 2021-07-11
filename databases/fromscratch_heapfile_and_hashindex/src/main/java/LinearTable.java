import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.List;

public class LinearTable {
    private final int SIZE = 1000000;
    private final int BUCKET_SIZE = 5 * Bucket.PAIR_LEN;
    private Bucket[] table = new Bucket[SIZE];

    public int hashingCode(String key) {
        return Math.abs(key.hashCode()) % SIZE;
    }

    public boolean add(String key, String data) {
        int probe;

        int code = this.hashingCode(key);

        if (table[code] == null) {
            table[code] = new Bucket();
            table[code].add(key, data);
            System.err.format("Adding recordLoc for %s as %s\n", key, data);
            probe = -1;
        } else if (!table[code].full()) {
            table[code].add(key, data);
            probe = -1;
        } else {
            probe = (code == table.length -1) ? 0 : code + 1;
        }

        while (probe != -1 && probe != code) {
            if (table[probe] == null) {
                table[code] = new Bucket();
                table[code].add(key, data);
                System.err.format("Adding recordLoc for %s as %s\n", key, data);
                break; // NOTE: assuming there's always room
            } else if (!table[code].full()) {
                System.err.format("Adding recordLoc for %s as %s\n", key, data);
                table[code].add(key, data);
                break;
            } else {
                if (probe == (table.length -1) )
                    probe = 0;
                else
                    probe++;

            }
        }

        if (probe != -1) return false;
        else return true;
    }

    public List<String> retrieve(String key) {
        int probe;

        int code = this.hashingCode(key);

        if (table[code] == null) {
            return null;
        }

        probe = code;

        List<String> match;
        while (table[probe] != null) {
            return table[probe].find(key);
        }

        return null;
    }

    public List<String> retrieveFromDisk(String target, String filepath) throws IOException {
        int code = hashingCode(target);
        byte[] bucketBytes = new byte[BUCKET_SIZE];

        RandomAccessFile raf = new RandomAccessFile(filepath, "r");

        int currOffset = BUCKET_SIZE * code;
        raf.seek(currOffset);
        raf.read(bucketBytes);
        int probe = (code + 1) % SIZE;

        Bucket currBucket = new Bucket(bucketBytes);
        while (!currBucket.empty()) {
            List<String> res = currBucket.find(target);
            if (res != null) {
                return res;
            }

            raf.seek(BUCKET_SIZE * probe);
            raf.read(bucketBytes);
            currBucket = new Bucket(bucketBytes);
            probe += 1;
        }

        return null; // TODO fix
    }

    private void clearData(String filepath) {
        // Truncate the file in-case it's not empty
        try {
            FileWriter f = new FileWriter(filepath);
            f.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void write(String filepath) throws IOException {
        clearData(filepath);
        FileOutputStream output = new FileOutputStream(filepath, true);
        try {
            for (int i = 0; i < table.length; i++) {
                if (table[i] != null) {
                    table[i].write(output);
                } else {
                    // write empty data into bucket position
                    output.write(new byte[BUCKET_SIZE]);
                }
            }
        } finally {
            output.close();
        }
    }

    public static void main(String[] args) {
        LinearTable index = new LinearTable();

        index.add("hello world", "12435");
        index.add("hello daisy", "54321");
        System.out.println(index.retrieve("hello daisy"));

//        System.out.println("Writing....");
//        String indexfp = "index.blah";
//        try {
//            index.write(indexfp);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }

        try {
            System.out.println("Finding....");
            List<String> res = index.retrieveFromDisk("drewz brewz", "hash.4096");
            for (String r : res) {
                System.out.println(r);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
