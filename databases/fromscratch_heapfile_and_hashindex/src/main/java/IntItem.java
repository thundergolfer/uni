import java.io.DataOutputStream;
import java.io.IOException;

public class IntItem implements Item {
    private static final long serialVersionUID = 1L;
    private final int val;

    public int getValue() {
        return val;
    }

    public IntItem(int i) {
        val = i;
    }

    public String toString() {
        return Integer.toString(val);
    }

    public void serialize(DataOutputStream dos) throws IOException {
        dos.writeInt(val);
    }

    public String getType() {
        return "INT";
    }

    public int length() {
        return 4; // Integers are stored as 4-bytes
    }

}
