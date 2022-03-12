enum TokenType {
    // Single character tokens
    COMMAND, SIMPLE_STRING_DATATYPE_ID,
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

    public String toString() {
        return type + " " + lexeme + " " + literal;
    }
}
