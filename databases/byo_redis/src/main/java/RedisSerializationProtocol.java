package com.thundergolfer.uni.byo.redis;

import java.util.ArrayList;
import java.util.List;

public class RedisSerializationProtocol {
    private static final String CRLF = "\r\n";

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
}
