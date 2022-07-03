use crate::scanner::TokenType::{TokenEOF, TokenIdentifier};

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TokenType {
    // Single-character tokens.
    TokenLeftParen,
    TokenRightParen,
    TokenLeftBrace,
    TokenRightBrace,
    TokenComma,
    TokenDot,
    TokenSemicolon,
    TokenMinus,
    TokenPlus,
    TokenSlash,
    TokenStar,
    // One or two character tokens.
    TokenBang,
    TokenBangEqual,
    TokenEqual,
    TokenEqualEqual,
    TokenGreater,
    TokenGreaterEqual,
    TokenLess,
    TokenLessEqual,
    // Literals.
    TokenIdentifier,
    TokenString,
    TokenNumber,
    // Keywords.
    TokenAnd,
    TokenClass,
    TokenElse,
    TokenFalse,
    TokenFor,
    TokenFun,
    TokenIf,
    TokenNil,
    TokenOr,
    TokenPrint,
    TokenReturn,
    TokenSuper,
    TokenThis,
    TokenTrue,
    TokenVar,
    TokenWhile,
    // Misc.
    TokenError,
    TokenEOF,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub token_type: TokenType,
    pub line: usize,
    // TODO(Jonathon): Should be &'a str not String.
    pub lexeme: String,
}

#[derive(Debug, Clone, Copy)]
pub struct Scanner<'a> {
    source: &'a str,
    line: usize,
    start: usize,
    current: usize,
}

impl<'a> Scanner<'_> {
    pub fn new(source: &'a str) -> Scanner<'_> {
        Scanner {
            source,
            line: 1,
            start: 0,
            current: 0,
        }
    }

    pub fn scan_token(&mut self) -> Token {
        self.skip_whitespace();
        self.start = self.current;

        if self.is_at_end() {
            return self.make_token(TokenEOF);
        }

        let c = self.advance();
        if is_alpha(c) {
            return self.make_identifier_token();
        }
        if is_digit(c) {
            return self.make_number_token();
        };

        match c {
            b'(' => self.make_token(TokenType::TokenLeftParen),
            b')' => self.make_token(TokenType::TokenRightParen),
            b'{' => self.make_token(TokenType::TokenLeftBrace),
            b'}' => self.make_token(TokenType::TokenRightBrace),
            b';' => self.make_token(TokenType::TokenSemicolon),
            b',' => self.make_token(TokenType::TokenComma),
            b'.' => self.make_token(TokenType::TokenDot),
            b'-' => self.make_token(TokenType::TokenMinus),
            b'+' => self.make_token(TokenType::TokenPlus),
            b'/' => self.make_token(TokenType::TokenSlash),
            b'*' => self.make_token(TokenType::TokenStar),
            b'!' => {
                let tkn_type = if self.match_char(b'=') {
                    TokenType::TokenBangEqual
                } else {
                    TokenType::TokenBang
                };
                self.make_token(tkn_type)
            }
            b'=' => {
                let tkn_type = if self.match_char(b'=') {
                    TokenType::TokenEqualEqual
                } else {
                    TokenType::TokenEqual
                };
                self.make_token(tkn_type)
            }
            b'<' => {
                let tkn_type = if self.match_char(b'=') {
                    TokenType::TokenLessEqual
                } else {
                    TokenType::TokenLess
                };
                self.make_token(tkn_type)
            }
            b'>' => {
                let tkn_type = if self.match_char(b'=') {
                    TokenType::TokenGreaterEqual
                } else {
                    TokenType::TokenGreater
                };
                self.make_token(tkn_type)
            }
            b'"' => self.make_string_token(),
            _ => self.error_token("Unexpected character.".into()),
        }
    }

    fn advance(&mut self) -> u8 {
        let ret = self.peek().unwrap();
        self.current += 1;
        ret
    }

    fn error_token(&self, message: String) -> Token {
        Token {
            token_type: TokenType::TokenError,
            line: self.line,
            lexeme: message,
        }
    }

    fn is_at_end(&self) -> bool {
        self.current == self.source.len()
    }

    fn check_keyword(
        &self,
        start: usize,
        length: usize,
        rest: &str,
        keyword_type: TokenType,
    ) -> TokenType {
        if self.current - self.start == start + length {
            // Check that begin + length is within the array, since we already moved current exactly that far.
            let begin = self.start + start;
            if &self.source[begin..(begin + length)] == rest {
                return keyword_type;
            }
        }
        TokenIdentifier
    }

    fn get_identifier_type(&self) -> TokenType {
        match self.source.as_bytes()[self.start] {
            b'a' => self.check_keyword(1, 2, "nd", TokenType::TokenAnd),
            b'c' => self.check_keyword(1, 4, "lass", TokenType::TokenClass),
            b'e' => self.check_keyword(1, 3, "lse", TokenType::TokenElse),
            b'i' => self.check_keyword(1, 1, "f", TokenType::TokenIf),
            b'n' => self.check_keyword(1, 2, "il", TokenType::TokenNil),
            b'o' => self.check_keyword(1, 1, "r", TokenType::TokenOr),
            b'p' => self.check_keyword(1, 4, "rint", TokenType::TokenPrint),
            b'r' => self.check_keyword(1, 5, "eturn", TokenType::TokenReturn),
            b's' => self.check_keyword(1, 4, "uper", TokenType::TokenSuper),
            b'v' => self.check_keyword(1, 2, "ar", TokenType::TokenVar),
            b'w' => self.check_keyword(1, 4, "hile", TokenType::TokenWhile),
            b'f' => {
                if self.current - self.start > 1 {
                    // more than 1 char in this maybe keyword
                    match self.source.as_bytes()[self.start + 1] {
                        b'a' => self.check_keyword(2, 3, "lse", TokenType::TokenFalse),
                        b'o' => self.check_keyword(2, 1, "r", TokenType::TokenFor),
                        b'u' => self.check_keyword(2, 1, "n", TokenType::TokenFun),
                        _ => TokenIdentifier,
                    }
                } else {
                    TokenIdentifier
                }
            }
            b't' => {
                if self.current - self.start > 1 {
                    // more than 1 char in this maybe keyword
                    match self.source.as_bytes()[self.start + 1] {
                        b'h' => self.check_keyword(2, 2, "is", TokenType::TokenThis),
                        b'r' => self.check_keyword(2, 2, "ue", TokenType::TokenTrue),
                        _ => TokenIdentifier,
                    }
                } else {
                    TokenIdentifier
                }
            }
            _ => TokenIdentifier,
        }
    }

    fn make_identifier_token(&mut self) -> Token {
        while matches!(self.peek(), Some(c) if is_alpha(c) || is_digit(c)) {
            self.advance();
        }
        self.make_token(self.get_identifier_type())
    }

    fn make_number_token(&mut self) -> Token {
        while matches!(self.peek(), Some(c) if is_digit(c)) {
            self.advance();
        }
        // Look for a fractional part.
        if matches!(self.peek(), Some(b'.')) {
            if let Some(ch) = self.peek_next() {
                if is_digit(ch) {
                    // Consume the ".".
                    self.advance();
                    while matches!(self.peek(), Some(c) if is_digit(c)) {
                        self.advance();
                    }
                }
            }
        }
        self.make_token(TokenType::TokenNumber)
    }

    fn make_string_token(&mut self) -> Token {
        while !matches!(self.peek(), Some(b'"')) {
            if let Some(b'\n') = self.peek() {
                self.line += 1;
            }
            self.advance();
        }
        if self.is_at_end() {
            return self.error_token("Unterminated string.".to_string());
        }
        // The closing quote.
        self.advance();
        self.make_token(TokenType::TokenString)
    }

    fn make_token(&self, token_type: TokenType) -> Token {
        Token {
            token_type,
            line: self.line,
            lexeme: self.source[self.start..self.current].to_string(),
        }
    }

    fn match_char(&mut self, expected: u8) -> bool {
        if matches!(self.peek(), Some(c) if c == expected) {
            self.current += 1;
            true
        } else {
            false
        }
    }

    fn peek(&self) -> Option<u8> {
        self.source.as_bytes().get(self.current).map(|char| *char)
    }

    fn peek_next(&self) -> Option<u8> {
        if self.current + 2 <= self.source.len() {
            Some(self.source.as_bytes()[self.current + 1])
        } else {
            None
        }
    }

    fn skip_whitespace(&mut self) {
        loop {
            if self.is_at_end() {
                break;
            }
            let c = self.peek().unwrap();
            match c {
                b' ' | b'\r' | b'\t' => {
                    self.advance();
                    break;
                }
                b'\n' => {
                    self.line += 1;
                    self.advance();
                    break;
                }
                b'/' => {
                    if let Some(b'/') = self.peek_next() {
                        while !matches!(self.peek(), Some(b'\n')) {
                            self.advance();
                        }
                    } else {
                        return;
                    }
                    break;
                }
                _ => break,
            }
        }
    }
}

fn is_digit(c: u8) -> bool {
    c >= b'0' && c <= b'9'
}

fn is_alpha(c: u8) -> bool {
    (c >= b'a' && c <= b'z') || (c >= b'A' && c <= b'Z') || c == b'_'
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::scanner::TokenType::{TokenEqual, TokenNumber, TokenSemicolon, TokenVar};

    #[test]
    fn test_scanner_scans_empty_source() {
        let mut scanner = Scanner::new("");
        let actual = scanner.scan_token();
        let expected = Token {
            line: 1,
            token_type: TokenEOF,
            lexeme: "".to_string(),
        };
        assert_eq!(expected, actual)
    }

    #[test]
    fn test_scanner_scans_numbers() {
        let mut scanner = Scanner::new("123.456");
        let actual = scanner.scan_token();
        let expected = Token {
            line: 1,
            token_type: TokenNumber,
            lexeme: "123.456".to_string(),
        };
        assert_eq!(expected, actual);

        let mut scanner = Scanner::new("99999;");
        let actual = scanner.scan_token();
        let expected = Token {
            line: 1,
            token_type: TokenNumber,
            lexeme: "99999".to_string(),
        };
        assert_eq!(expected, actual);
    }

    #[test]
    fn test_scans_expression() {
        let mut actual_tokens: Vec<Token> = Vec::new();
        let mut scanner = Scanner::new("var foo = 1.2;");
        loop {
            let t = scanner.scan_token();
            actual_tokens.push(t);
            if actual_tokens.last().unwrap().token_type == TokenEOF {
                break;
            }
        }
        let expected_tokens = vec![
            Token {
                line: 1,
                token_type: TokenVar,
                lexeme: "var".to_string(),
            },
            Token {
                line: 1,
                token_type: TokenIdentifier,
                lexeme: "foo".to_string(),
            },
            Token {
                line: 1,
                token_type: TokenEqual,
                lexeme: "=".to_string(),
            },
            Token {
                line: 1,
                token_type: TokenNumber,
                lexeme: "1.2".to_string(),
            },
            Token {
                line: 1,
                token_type: TokenSemicolon,
                lexeme: ";".to_string(),
            },
            Token {
                line: 1,
                token_type: TokenEOF,
                lexeme: "".to_string(),
            },
        ];
        assert_eq!(actual_tokens, expected_tokens);
    }
}
