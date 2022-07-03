use crate::chunk::Chunk;
use crate::scanner::{self, Scanner, Token, TokenType};

pub struct Parser<'code> {
    current: Option<Token>,
    previous: Option<Token>,
    scanner: Scanner<'code>,
    had_error: bool,
    panic_mode: bool,
}

impl<'code> Parser<'code> {
    pub fn new(scanner: Scanner) -> Parser {
        Parser {
            current: None,
            previous: None,
            scanner,
            had_error: false,
            panic_mode: false,
        }
    }

    pub fn advance(&mut self) {
        self.previous = self.current.take();
        loop {
            self.current = Some(self.scanner.scan_token());
            if self.current.as_ref().unwrap().token_type != TokenType::TokenError {
                break;
            }
            // TODO(Jonathon): Awful avoidance of borrow checker.
            let msg = self.current.as_ref().unwrap().lexeme.clone();
            self.error_at_current(msg.as_str());
        }
    }

    fn error_at_current(&mut self, message: &str) {
        self.error_at(self.current.as_ref().unwrap().clone(), message);
    }

    fn error(&mut self, message: &str) {
        self.error_at(self.previous.as_ref().unwrap().clone(), message);
    }

    fn error_at(&mut self, token: Token, message: &str) {
        if self.panic_mode {
            return;
        }
        self.panic_mode = true;
        eprint!("[line {}] Error", token.line);
        match token.token_type {
            TokenType::TokenEOF => eprint!(" at end"),
            TokenType::TokenError => {}
            _ => eprint!(" at '{}'", token.lexeme),
        }
        eprintln!(": {}", message);
        self.had_error = true;
    }
}

pub fn compile(source: &str, chunk: &Chunk) -> bool {
    let scanner = scanner::Scanner::new(source);
    let mut parser = Parser::new(scanner);
    parser.advance();
    expression();
    consume(TokenType::TokenEOF, "Expect end of expression");
    true
}

fn advance() {}
fn expression() {}
fn consume(token_type: TokenType, error_msg: &str) {}
