package me.serce;

import org.openjdk.jmh.annotations.*;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.LongBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Paths;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;

import static java.nio.file.StandardOpenOption.READ;

@Fork(1)
@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 5, timeUnit = TimeUnit.MILLISECONDS)
@Measurement(iterations = 5, timeUnit = TimeUnit.MILLISECONDS)
public class OrderBenchmark {

  public static final int SIZE = 1024 * 1024 * 1024;

  @Param({"direct-native-order", "direct"})
  String bufferType;
  
  FileChannel channel;
  LongBuffer buffer;

  @Setup
  public void setUp() throws IOException {
    ByteBuffer buffer;
    switch (bufferType) {
      case "direct": buffer = ByteBuffer.allocateDirect(SIZE);
        break;
      case "direct-native-order":
        buffer = ByteBuffer.allocateDirect(SIZE).order(ByteOrder.nativeOrder());
        break;
      default:
        throw new AssertionError();
    }
    channel = FileChannel.open(Paths.get("/dev/urandom"), READ);
    while (buffer.hasRemaining()) {
      channel.read(buffer);
    }
    buffer.flip();
    this.buffer = buffer.asLongBuffer();
  }

  @TearDown
  public void tearDown() throws IOException {
    channel.close();
  }

  @Fork(jvmArgsAppend = {
      "-XX:+UnlockDiagnosticVMOptions",
      "-XX:PrintAssemblyOptions=intel",
      "-XX:CompileCommand=print,*OrderBenchmark.sumBytes*",
  })
  @Benchmark
  public long sumBytes() throws Exception {
    long sum = 0;
    for (int i = 0; i < SIZE / 8; i++) {
      sum += buffer.get(i);
    }
    return sum;
  }
}
