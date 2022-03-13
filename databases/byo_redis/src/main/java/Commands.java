package com.thundergolfer.uni.byo.redis;

import java.util.ArrayList;
import java.util.List;

public class Commands {
    public static String runCommand(Datastore store, List<RedisData> command) throws CommandException {
        if (command.size() == 0) return RedisSerializationProtocol.SimpleString.create("EMPTY");

        String commandStr;
        if (command.get(0).getType() != RedisDataType.SIMPLE_STRING) {
            throw new CommandException("Invalid command. Expected command string as 1st arg.");
        } else {
            commandStr = command.get(0).getStrValue();
        }

        RedisCmd c;
        try {
            c = RedisCmd.valueOf(commandStr.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new CommandException(String.format("Unhandled command: %s", commandStr));
        }
        List<String> args= redisDataToStringArgs(command.subList(1, command.size()));
        switch (c) {
            case ECHO:
                return runECHO(args);
            case PING:
                return runPING(args);
            case SET:
                return runSET(store, args);
            case GET:
                return runGET(store, args);
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

    // TODO(Jonathon): Support expiry, the final challenge of https://app.codecrafters.io/courses/redis.
    private static String runSET(Datastore store, List<String> args) throws CommandException {
        if (args.size() != 2) {
            throw new CommandException("Invalid SET command. Must be 'SET <key> <value>.");
        }
        String key = args.get(0);
        String value = args.get(1);
        store.set(key, value);
        return RedisSerializationProtocol.SimpleString.Ok();
    }

    private static String runGET(Datastore store, List<String> args) throws CommandException {
        if (args.size() != 1) {
            throw new CommandException("Invalid GET command. Must be 'GET <key>.");
        }
        String key = args.get(0);
        String val = store.get(key);
        if (val == null) {
            return RedisSerializationProtocol.BulkString.Nil();
        } else {
            return RedisSerializationProtocol.BulkString.create(val);
        }
    }
}


enum RedisCmd {
    PING,
    ECHO,
    GET,
    SET,
}
