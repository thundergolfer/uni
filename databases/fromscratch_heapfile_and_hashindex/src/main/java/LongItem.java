import java.io.DataOutputStream;
import java.io.IOException;

public class LongItem implements Item {
    private static final long serialVersionUID = 1L;
    private final long val;

    public long getValue() {
        return val;
    }

    public LongItem(long i) {
        val = i;
    }

    public String toString() {
        return Long.toString(val);
    }

    public void serialize(DataOutputStream dos) throws IOException {
        dos.writeLong(val);
    }

    public String getType() {
        return "LONG";
    }

    public int length() {
        return 8; // Longs are stored as 8-bytes
    }

}
