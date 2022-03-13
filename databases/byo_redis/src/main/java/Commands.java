package com.thundergolfer.uni.byo.redis;

import java.util.ArrayList;
import java.util.List;

public class Commands {
    public static String runCommand(List<RedisData> command) throws CommandException {
        System.out.println("Running command...");
        System.out.println(command);
        if (command.size() == 0) return RedisSerializationProtocol.SimpleString.create("EMPTY");

        String commandStr;
        if (command.get(0).getType() != RedisDataType.SIMPLE_STRING) {
            throw new CommandException("Invalid command. Expected command string as 1st arg.");
        } else {
            commandStr = command.get(0).getStrValue();
        }

        COMMAND c;
        try {
            c = COMMAND.valueOf(commandStr.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new CommandException(String.format("Unhandled command: %s", commandStr));
        }

        List<String> args;
        switch (c) {
            case ECHO:
                args = redisDataToStringArgs(command.subList(1, command.size()));
                return runECHO(args);
            case PING:
                args = redisDataToStringArgs(command.subList(1, command.size()));
                return runPING(args);
            default:
                throw new AssertionError("Enum match failed.");
        }
    }

    private static List<String> redisDataToStringArgs(List<RedisData> data) throws CommandException {
        List<String> args = new ArrayList<>();
        for (RedisData d : data) {
            if (d.getType() != RedisDataType.SIMPLE_STRING) {
                throw new CommandException("Got non-string argument in strings-only command.");
            }
            args.add(d.getStrValue());
        }
        return args;
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

    private static String runECHO(List<String> args) throws CommandException {
        String message = String.join(" ", args);
        return RedisSerializationProtocol.BulkString.create(message);
    }

    private static String runPING(List<String> args) throws CommandException {
        // EOF only argument
        System.err.println(args);
        if (args == null || args.size() == 0) {
            return RedisSerializationProtocol.SimpleString.create("PONG");
        } else {
            throw new CommandException("Arguments are not supported for PING command.");
        }
    }
}


enum COMMAND {
    PING,
    ECHO,
}
