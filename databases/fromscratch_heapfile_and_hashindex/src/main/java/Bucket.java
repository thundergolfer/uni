import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Bucket {
    private int capacity;
    private byte data[];
    private int nextFree;
    private int freeSlots;

    private static int MAX_KEY_LEN = 256;
    private static int MAX_LOCATION_LEN = 12;
    public static int PAIR_LEN = MAX_KEY_LEN + MAX_LOCATION_LEN;

    public Bucket(byte[] data) {
        this.data = data;
        this.capacity = data.length / PAIR_LEN;
    }

    public Bucket(int capacity) {
        this.capacity = capacity;
        this.data = new byte[this.capacity * (PAIR_LEN)];
        this.nextFree = 0;
        this.freeSlots = this.capacity;
    }

    public Bucket() {
        this(5);
    }

    public boolean add(String key, String data) {
        byte[] byteKey = toBytes(key, MAX_KEY_LEN);
        byte[] byteLoc = toBytes(data, MAX_LOCATION_LEN);

        System.arraycopy(byteKey, 0, this.data, this.nextFree, MAX_KEY_LEN);
        this.nextFree += MAX_KEY_LEN;
        System.arraycopy(byteLoc, 0, this.data, this.nextFree, MAX_LOCATION_LEN);
        this.nextFree += MAX_LOCATION_LEN;
        this.freeSlots -= 1;
        return true; // TODO
    }

    public List<String> find(String target) {
        List<String> lst = new ArrayList<>();
        if (empty()) {
            return lst;
        }

        String key;
        for (int i = 0; i < this.capacity - this.freeSlots; i++) {
            byte[] keyBytes = new byte[MAX_KEY_LEN];
            System.arraycopy(this.data, i * PAIR_LEN, keyBytes, 0, MAX_KEY_LEN);
            key = new String(trim(keyBytes), StandardCharsets.UTF_8);
            if (key.equals(target)) {
                byte[] locBytes = new byte[MAX_LOCATION_LEN];
                System.arraycopy(this.data, (i * PAIR_LEN) + MAX_KEY_LEN, locBytes, 0, MAX_LOCATION_LEN);
                String loc = new String(trim(locBytes), StandardCharsets.UTF_8);
                lst.add(loc);
            }
        }
        return lst;
    }

    public boolean full() {
        // would it's current data + another recordLocator cause the bucket to be > 70% full?
        float fillLevel = (this.capacity - this.freeSlots) / (float) this.capacity;
        if (fillLevel > 0.7) {
            return true;
        }
        return false;
    }

    public boolean empty() {
        return this.data[0] == 0;
    }

    private static byte[] toBytes(String data, int length) {
        byte[] result = new byte[length];
        System.arraycopy(data.getBytes(), 0, result, 0, data.length());
        return result;
    }

    private static byte[] trim(byte[] bytes) {
        int i = bytes.length - 1;
        while (i >= 0 && bytes[i] == 0) {
            --i;
        }
        return Arrays.copyOf(bytes, i + 1);
    }

    public void write(FileOutputStream output) throws IOException {
        output.write(this.data);
    }

    public static void main(String[] args) {
        Bucket b = new Bucket();

        System.out.println(b.find("my friend"));
        b.add("hello world", "13043");
        b.add("hello daisy", "13323");
        System.out.println(b.find("hello daisy"));
        b.add("hello world", "11111");
        b.add("hello daisy", "12232");
        b.add("hello jack", "66666");
        System.out.println(b.full());
        System.out.println(b.find("hello daisy"));
    }

}
