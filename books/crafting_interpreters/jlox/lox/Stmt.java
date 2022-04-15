package com.craftinginterpreters.lox;

import java.util.List;

abstract class Stmt {
  interface Visitor<R> {
    R visitExpressionStmt(Expression stmt);
    R visitFunctionStmt(Function stmt);
    R visitIfStmt(If stmt);
    R visitBlockStmt(Block stmt);
    R visitClassStmt(Class stmt);
    R visitPrintStmt(Print stmt);
    R visitReturnStmt(Return stmt);
    R visitWhileStmt(While stmt);
    R visitVarStmt(Var stmt);
  }

  static class Expression extends Stmt {
    Expression(Expr expression) {
    this.expression = expression;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitExpressionStmt(this);
    }

    final Expr expression;
  }

  static class Function extends Stmt {
    Function(Token name, List<Token> params, List<Stmt> body) {
    this.name = name;
    this.params = params;
    this.body = body;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitFunctionStmt(this);
    }

    final Token name;
    final List<Token> params;
    final List<Stmt> body;
  }

  static class If extends Stmt {
    If(Expr condition, Stmt thenBranch, Stmt elseBranch) {
    this.condition = condition;
    this.thenBranch = thenBranch;
    this.elseBranch = elseBranch;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitIfStmt(this);
    }

    final Expr condition;
    final Stmt thenBranch;
    final Stmt elseBranch;
  }

  static class Block extends Stmt {
    Block(List<Stmt> statements) {
    this.statements = statements;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitBlockStmt(this);
    }

    final List<Stmt> statements;
  }

  static class Class extends Stmt {
    Class(Token name, Expr.Variable superclass, List<Stmt.Function> methods) {
    this.name = name;
    this.superclass = superclass;
    this.methods = methods;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitClassStmt(this);
    }

    final Token name;
    final Expr.Variable superclass;
    final List<Stmt.Function> methods;
  }

  static class Print extends Stmt {
    Print(Expr expression) {
    this.expression = expression;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitPrintStmt(this);
    }

    final Expr expression;
  }

  static class Return extends Stmt {
    Return(Token keyword, Expr value) {
    this.keyword = keyword;
    this.value = value;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitReturnStmt(this);
    }

    final Token keyword;
    final Expr value;
  }

  static class While extends Stmt {
    While(Expr condition, Stmt body) {
    this.condition = condition;
    this.body = body;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitWhileStmt(this);
    }

    final Expr condition;
    final Stmt body;
  }

  static class Var extends Stmt {
    Var(Token name, Expr initializer) {
    this.name = name;
    this.initializer = initializer;
    }

    @Override
    <R> R accept(Visitor<R> visitor) {
      return visitor.visitVarStmt(this);
    }

    final Token name;
    final Expr initializer;
  }

  abstract <R> R accept(Visitor<R> visitor);
}
