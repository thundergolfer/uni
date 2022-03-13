package com.thundergolfer.uni.byo.redis;

import java.util.ArrayList;
import java.util.List;

public class Scanner {
    private final String source;
    private final List<Token> tokens = new ArrayList<>();

    private int start = 0;
    private int current = 0;
    private int line = 1;

    Scanner(String source) {
        this.source = source;
    }

    List<Token> scanTokens() throws ScannerException {
        while (!isAtEnd()) {
            // We are at the beginning of the next lexeme;
            start = current;
            scanToken();
        }

        tokens.add(new Token(TokenType.EOF, "", null, line));
        return tokens;
    }

    private void string() throws ScannerException {
        while (peek() != '"' && !isAtEnd()) {
            if (peek() == '\n') line++;
            advance();
        }

        if (isAtEnd()) {
            throw new ScannerException("Could not scan input.");
        }
        advance(); // the closing " character.
        // Trim the surrounding quotes.
        String value = source.substring(start + 1, current - 1);
        addToken(TokenType.STRING, value);
    }

    private char peek() {
        if (isAtEnd()) return '\0';
        return source.charAt(current);
    }

    private void addToken(TokenType type) {
        addToken(type, null);
    }

    private void addToken(TokenType type, Object literal) {
        String text = source.substring(start, current);
        tokens.add(new Token(type, text, literal, line));
    }

    private void scanToken() throws ScannerException {
        char c = advance();
        switch (c) {
            case '"': string(); break;
            case '+': addToken(TokenType.SIMPLE_STRING_DATATYPE_ID); break;
            case '-': addToken(TokenType.ERROR_DATATYPE_ID); break;
            case '*': addToken(TokenType.ARRAYS_DATATYPE_ID); break;
            case ':': addToken(TokenType.INT_DATATYPE_ID); break;
            case '$': addToken(TokenType.BULK_STRING_DATATYPE_ID); break;
            case ' ':
                // Ignore whitespace.
                break;
            default:
                if (isDigit(c)) {
                    number();
                } else if (isAlpha(c)) {
                    identifier();
                } else {
                    throw new ScannerException("Could not scan input.");
                }
                break;
        }
    }

    private char peekNext() {
        if (current + 1 >= source.length()) return '\0';
        return source.charAt(current + 1);
    }

    private void number() {
        while (isDigit(peek())) advance();

        // Look for a fractional part.
        if (peek() == '.' && isDigit(peekNext())) {
            // Consume the "."
            advance();

            while (isDigit(peek())) advance();
        }

        addToken(TokenType.NUMBER,
                Integer.parseInt(source.substring(start, current)));
    }

    private boolean isAlpha(char c) {
        return (c >= 'a' && c <= 'z') ||
                (c >= 'A' && c <= 'Z') ||
                c == '_';
    }

    private boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }

    private boolean isAlphaNumeric(char c) {
        return isDigit(c) || isAlpha(c);
    }

    private void identifier() {
        while (isAlphaNumeric(peek())) advance();
        addToken(TokenType.IDENTIFIER);
    }

    private char advance() {
        return source.charAt(current++);
    }

    private boolean isAtEnd() {
        return current >= source.length();
    }
}
