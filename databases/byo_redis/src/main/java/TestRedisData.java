package com.thundergolfer.uni.byo.redis;

import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;

public class TestRedisData {
    @Test
    public void testFoo() {
        assertEquals(1, 1);
    }

    @Test
    public void testDeserPingCommandDataFromRESPArray() {
        List<Token> lineOne = Arrays.asList(
                new Token(TokenType.ARRAYS_DATATYPE_ID, "*", null, 0),
                new Token(TokenType.NUMBER, "1", 1, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> lineTwo = Arrays.asList(
                new Token(TokenType.BULK_STRING_DATATYPE_ID, "$", null, 0),
                new Token(TokenType.NUMBER, "4", 4, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> lineThree = Arrays.asList(
                new Token(TokenType.IDENTIFIER, "ping", null, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        RedisData.Deserializer deserializer = new RedisData.Deserializer();
        deserializer.process(lineOne);
        deserializer.process(lineTwo);
        deserializer.process(lineThree);
        List<RedisData> actual = deserializer.getRedisData();
        assertEquals(1, actual.size());
        assertEquals(RedisDataType.SIMPLE_STRING, actual.get(0).getType());
        assertEquals("ping", actual.get(0).getStrValue());
    }

    @Test
    public void testDeserECHOCommandDataFromRESPArray() {
        List<Token> lineOne = Arrays.asList(
                new Token(TokenType.ARRAYS_DATATYPE_ID, "*", null, 0),
                new Token(TokenType.NUMBER, "2", 2, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> lineTwo = Arrays.asList(
                new Token(TokenType.BULK_STRING_DATATYPE_ID, "$", null, 0),
                new Token(TokenType.NUMBER, "4", 4, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> lineThree = Arrays.asList(
                new Token(TokenType.IDENTIFIER, "ECHO", null, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> lineFour = Arrays.asList(
                new Token(TokenType.BULK_STRING_DATATYPE_ID, "$", null, 0),
                new Token(TokenType.NUMBER, "5", 4, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> lineFive = Arrays.asList(
                new Token(TokenType.IDENTIFIER, "Hello", null, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        RedisData.Deserializer deserializer = new RedisData.Deserializer();
        deserializer.process(lineOne);
        deserializer.process(lineTwo);
        deserializer.process(lineThree);
        deserializer.process(lineFour);
        deserializer.process(lineFive);
        List<RedisData> actual = deserializer.getRedisData();
        assertEquals(2, actual.size());
        assertEquals(RedisDataType.SIMPLE_STRING, actual.get(0).getType());
        assertEquals("ECHO", actual.get(0).getStrValue());
        assertEquals(RedisDataType.SIMPLE_STRING, actual.get(1).getType());
        assertEquals("Hello", actual.get(1).getStrValue());
    }
}
