use crate::scanner::TokenType::{TokenEOF, TokenElse};

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

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub line: usize,
    // TODO(Jonathon): Should be &'a str or something not String.
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
        let ret = self.peek();
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

    fn make_number_token(&mut self) -> Token {
        while is_digit(self.peek()) {
            self.advance();
        }

        // Look for a fractional part.
        if self.peek() == b'.' {
            if let Some(ch) = self.peek_next() {
                if is_digit(ch) {
                    // Consume the ".".
                    self.advance();

                    while !self.is_at_end() && is_digit(self.peek()) {
                        self.advance();
                    }
                }
            }
        }

        self.make_token(TokenType::TokenNumber)
    }

    fn make_string_token(&mut self) -> Token {
        while !self.is_at_end() && self.peek() != b'"' {
            if self.peek() == b'\n' {
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
        return if self.is_at_end() {
            false
        } else if self.peek() != expected {
            false
        } else {
            self.current += 1;
            true
        };
    }

    fn peek(&self) -> u8 {
        self.source.as_bytes()[self.current]
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
            let c = self.peek();
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
                        while self.peek() != b'\n' && !self.is_at_end() {
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
