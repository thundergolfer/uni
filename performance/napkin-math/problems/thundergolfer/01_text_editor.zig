const std = @import("std");
const test_allocator = std.testing.allocator;

pub fn oom() noreturn {
    @panic("Out of memory");
}

fn rawInsert(buffer: *std.ArrayList(u8), pos: usize, bytes: []const u8) void {
    buffer.resize(buffer.items.len + bytes.len) catch oom();
    std.mem.copyBackwards(u8, buffer.items[pos + bytes.len ..], buffer.items[pos .. buffer.items.len - bytes.len]);
    std.mem.copy(u8, buffer.items[pos..], bytes);
}

pub fn main() void {
    var list = std.ArrayList(u8).init(test_allocator);
    defer list.deinit();
    list.appendSlice("Hello, World!") catch oom();
    var string = "abc";

    // TODO(Jonathon): Make this a performance test by inserting some string at the beginning of a 1MB
    // text buffer and timing it.
    //
    // Also check the assembly to understand
    rawInsert(&list, 2, string);

    std.debug.print("{s}\n", .{list.items});
}
