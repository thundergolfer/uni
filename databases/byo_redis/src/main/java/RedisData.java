package com.thundergolfer.uni.byo.redis;

import java.util.List;

enum RedisDataType {
    SIMPLE_STRING,
    BULK_STRING, // TODO(Jonathon): Stop handling all strings the same.
    INTEGER,
    ARRAY,
}

public class RedisData {
    private RedisDataType type;
    private String strValue;
    private Integer intValue;
    private List<RedisData> arrValue;

    public RedisData(String val) {
        this.type = RedisDataType.SIMPLE_STRING;
        this.strValue = val;
        this.intValue = null;
        this.arrValue = null;
    }

    public RedisData(int val) {
        this.type = RedisDataType.INTEGER;
        this.strValue = null;
        this.intValue = val;
        this.arrValue = null;
    }

    public RedisData(List<RedisData> val) {
        this.type = RedisDataType.ARRAY;
        this.strValue = null;
        this.intValue = null;
        this.arrValue = val;
    }

    public RedisDataType getType() {
        return this.type;
    }

    public static RedisData from(List<Token> tokens) {
        return null; // TODO
    }

    public static RedisData from(RedisSerializationProtocol.Array RESPArr) {
        return null; // TODO
    }
}
