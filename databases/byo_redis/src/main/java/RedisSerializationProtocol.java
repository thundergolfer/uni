import java.util.ArrayList;
import java.util.List;

public class RedisSerializationProtocol {
    private static final String CRLF = "\r\n";

    public static boolean isRESPArray(List<Token> tokens) {
        return tokens.size() > 1 && tokens.get(0).type == TokenType.ARRAYS_DATATYPE_ID;
    }

    static class SimpleString {
        private static final char firstByte = '+';

        public static String Ok() {
            StringBuilder sb = new StringBuilder();
            sb.append(firstByte);
            sb.append("OK");
            sb.append(RedisSerializationProtocol.CRLF);
            return sb.toString();
        }

        public static String create(String message) {
            StringBuilder sb = new StringBuilder();
            sb.append(firstByte);
            sb.append(message);
            sb.append(RedisSerializationProtocol.CRLF);
            return sb.toString();
        }
    }

    static class BulkString {
        private static final char firstByte = '$';

        public static String create(String message) {
            StringBuilder sb = new StringBuilder();
            sb.append(firstByte);
            sb.append(message.length());
            sb.append(RedisSerializationProtocol.CRLF);
            sb.append(message);
            sb.append(RedisSerializationProtocol.CRLF);
            return sb.toString();
        }
    }

    static class Array {
        public int length;
        public List<List<Token>> items;
        private List<String> elements;

        Array(int length) {
            this.length = length;
            this.items = new ArrayList<>();
            this.elements = new ArrayList<>();
        }

        public void addItem(List<Token> item) {
            if (item.get(0).type != TokenType.BULK_STRING_DATATYPE_ID) {
                elements.add(item.get(1).lexeme);
            }
            items.add(item);
        }

        public boolean isFilled() {
            return this.elements.size() == this.length;
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (List<Token> item : items) {
                for (Token t : item) {
                    sb.append(t.toString());
                    sb.append(", ");
                }
                sb.append('\n');
            }
            return sb.toString();
        }
    }

}
