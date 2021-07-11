import java.io.Serializable;

import java.io.DataOutputStream;
import java.io.IOException;

public interface Item extends Serializable {
    void serialize(DataOutputStream dos) throws IOException;

    String getType();

    String toString();

    int length();
}
