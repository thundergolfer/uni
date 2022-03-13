package com.thundergolfer.uni.byo.redis;

import java.util.ArrayList;
import java.util.List;

enum RedisDataType {
    SIMPLE_STRING,
    BULK_STRING, // TODO(Jonathon): Stop handling all strings the same.
    INTEGER,
    ARRAY,
}

public class RedisData {
    static class Deserializer {
        private boolean isDeserializingBulkString;
        private int arrayLength;
        private List<RedisData> data;

        public Deserializer() {
            this.arrayLength = 1;
            this.data = new ArrayList<>();
        }

        public void reset() {
            this.arrayLength = 1;
            this.data.clear();
        }

        public void process(List<Token> tokens) {
            if (this.isComplete()) {
                throw new RuntimeException("Attempted further processing on complete deserialization.");
            }

            if (tokens.size() == 0) return;

            TokenType lineType = tokens.get(0).type;
            switch (lineType) {
                case ARRAYS_DATATYPE_ID:
                    processArrayStart(tokens);
                    break;
                case BULK_STRING_DATATYPE_ID:
                    processBulkStringStart(tokens);
                    break;
                case IDENTIFIER:
                    processIdentifier(tokens);
                    break;
                case NUMBER:
                    processNumber(tokens);
                    break;
                default:
                    throw new RuntimeException(String.format("Unsupported type %s", lineType));
            }
        }

        public List<RedisData> getRedisData() {
            if (!isComplete()) {
                throw new RuntimeException("Attempted access on incomplete deserialization.");
            }
            return this.data;
        }

        public boolean isComplete() {
            return this.data.size() == this.arrayLength;
        }

        private void processArrayStart(List<Token> tokens) {
            int arrLength = (int) tokens.get(1).literal;
            this.arrayLength = arrLength;
        }

        private void processBulkStringStart(List<Token> tokens) {
            int bulkStringLen = (int) tokens.get(1).literal;
            this.isDeserializingBulkString = true;
        }

        private void processBulkString(List<Token> tokens) {
            String val = tokens.get(0).lexeme;
            RedisData datum = new RedisData(val);
            this.data.add(datum);
            isDeserializingBulkString = false;
        }

        private void processIdentifier(List<Token> tokens) {
            if (isDeserializingBulkString) {
                processBulkString(tokens);
            } else {
                processSimpleString(tokens);
            }
        }

        private void processNumber(List<Token> tokens) {
            if (isDeserializingBulkString) {
                processBulkString(tokens);
            } else {
                processSimpleString(tokens);
            }
        }

        private void processSimpleString(List<Token> tokens) {
            String val = tokens.get(0).lexeme;
            RedisData datum = new RedisData(val);
            this.data.add(datum);
        }
    }

    private RedisDataType type;
    private String strValue;
    private Integer intValue;

    public RedisData(String val) {
        this.type = RedisDataType.SIMPLE_STRING;
        this.strValue = val;
        this.intValue = null;
    }

    public RedisData(int val) {
        this.type = RedisDataType.INTEGER;
        this.strValue = null;
        this.intValue = val;
    }

    public RedisData(List<RedisData> val) {
        this.type = RedisDataType.ARRAY;
        this.strValue = null;
        this.intValue = null;
    }

    public RedisDataType getType() {
        return this.type;
    }

    public String getStrValue() {
        return this.strValue;
    }

    public Integer getIntValue() {
        return this.intValue;
    }

    @Override
    public String toString() {
        if (this.getType() == RedisDataType.INTEGER) {
            return String.valueOf(this.intValue);
        } else {
            return this.strValue;
        }
    }
}
