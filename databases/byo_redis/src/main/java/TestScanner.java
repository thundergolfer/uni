package com.thundergolfer.uni.byo.redis;

import org.junit.Test;

import java.util.*;
import java.util.Collections;
import java.util.LinkedList;

import static org.junit.Assert.assertEquals;

public class TestScanner {
    @Test
    public void testScanSimpleStrinrg() throws ScannerException {
        String input = "+Hello";
        Scanner scanner = new Scanner(input);
        List<Token> expected = Arrays.asList(
                new Token(TokenType.SIMPLE_STRING_DATATYPE_ID, "+", null, 0),
                new Token(TokenType.IDENTIFIER, "Hello", null, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> actual = scanner.scanTokens();
        assertEquals(expected, actual);
    }

    @Test
    public void testScanArrayStarter() throws ScannerException {
        String input = "*9";
        Scanner scanner = new Scanner(input);
        List<Token> expected = Arrays.asList(
                new Token(TokenType.ARRAYS_DATATYPE_ID, "*", null, 0),
                new Token(TokenType.NUMBER, "9", 9.0, 0),
                new Token(TokenType.EOF, "", null, 0)
        );
        List<Token> actual = scanner.scanTokens();
        assertEquals(expected, actual);
    }
}
