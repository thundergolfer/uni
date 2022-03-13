package com.thundergolfer.uni.byo.redis;

import java.util.concurrent.ConcurrentHashMap;

public class Datastore {
    private ConcurrentHashMap<String, String> map;

    public Datastore() {
        this.map = new ConcurrentHashMap<>();
    }

    public void set(String key, String value) {
        this.map.put(key, value);
    }

    public String get(String key) {
        return this.map.get(key);
    }
}
