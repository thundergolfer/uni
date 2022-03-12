import java.util.ArrayList;
import java.util.List;

public class Commands {
    public static String runCommand(RedisSerializationProtocol.Array respArr) throws CommandException {
        List<String> commandArgs = new ArrayList<>();
        String command = null;
        String curr;
        for (List<Token> item : respArr.items) {
            curr = argumentFromTokens(item);
            if (curr != null) {
                if (command == null) {
                    command = curr;
                } else {
                    commandArgs.add(curr);
                }
            }
        }
        if (command.toUpperCase().equals("ECHO")) {
            System.out.println("Run ECHO with args" + commandArgs.toString());
            return runECHO(commandArgs);
        } else if (command.toUpperCase().equals("PING")) {
            return runPING(null);
        } else {
            throw new RuntimeException("Fuck command was not matched: " + command);
        }
    }

    private static String argumentFromTokens(List<Token> tokens) {
        Token valToken;
        if (tokens.get(0).type == TokenType.INT_DATATYPE_ID) {
            valToken = tokens.get(1);
            if (valToken.type == TokenType.NUMBER) {
                return String.valueOf(valToken.literal);
            } else {
                throw new RuntimeException("Fuck");
            }
        } else if (tokens.get(0).type == TokenType.BULK_STRING_DATATYPE_ID) {
            return null;
        } else if (tokens.get(0).type == TokenType.IDENTIFIER) {
            return tokens.get(0).lexeme;
        }
        return null;
    }

    public static String runCommand(List<Token> input) throws CommandException {
        if (input.size() == 0) {
            return "";
        }

        Token commandToken = input.get(0);
        if (commandToken.type == TokenType.COMMAND) {
            if (commandToken.lexeme.equals("PING")) {
                return runPING(input.subList(1, input.size()));
            } else {
                throw new CommandException(String.format("%s command not implemented.", commandToken.lexeme));
            }
        } else {
            throw new CommandException("Command not provided.");
        }
    }

    private static String runECHO(List<String> args) throws CommandException {
        return RedisSerializationProtocol.BulkString.create(args.get(0));
    }

    private static String runPING(List<Token> args) throws CommandException {
        // EOF only argument
        if (args == null || args.size() == 1) {
            return RedisSerializationProtocol.SimpleString.create("PONG");
        } else {
            throw new CommandException("Arguments are not supported for PING command.");
        }
    }
}
