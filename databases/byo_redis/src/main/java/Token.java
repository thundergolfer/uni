package com.thundergolfer.uni.byo.redis;

enum TokenType {
    // Single character tokens
    SIMPLE_STRING_DATATYPE_ID,
    ERROR_DATATYPE_ID, ARRAYS_DATATYPE_ID,
    BULK_STRING_DATATYPE_ID, INT_DATATYPE_ID,

    // One or two character tokens

    // Literals
    IDENTIFIER, STRING, NUMBER,

    // Keywords

    EOF
}

class Token {
    final TokenType type;
    final String lexeme;
    final Object literal;
    final int line;

    Token(TokenType type, String lexeme, Object literal, int line) {
        this.type = type;
        this.lexeme = lexeme;
        this.literal = literal;
        this.line = line;
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Token)) {
            return false;
        }
        if (obj == this) return true;

        Token other = (Token) obj;
        if (this.type != other.type) return false;
        if (!(this.lexeme.equals(other.lexeme))) return false;
        if (this.line == other.line) return false;
        if (this.literal == null && other.literal == null) return true;
        if (this.literal != null && this.literal.equals(other.literal)) return true;
        return false;
    }

    @Override
    public int hashCode() {
        int result = 17;
        result = 31 * result + this.type.hashCode();
        result = 31 * result + this.literal.hashCode();
        result = 31 * result + this.line;
        result = 31 * result + this.lexeme.hashCode();
        return result;
    }

    public String toString() {
        return type + " " + lexeme + " " + literal;
    }
}
