import java.io.DataOutputStream;
import java.io.IOException;

public class StringItem implements Item {
    private static final long serialVersionUID = 1L;
    private final String val;

    public String getValue() {
        return val;
    }

    public StringItem(String s) {
        val = s;
    }

    public String toString() {
        return val;
    }

    public void serialize(DataOutputStream dos) throws IOException {
//        dos.writeInt(s.length());
        dos.writeBytes(val);
    }

    public String getType() {
        return "TEXT";
    }

    public int length() {
        return val.length();
    }
}
