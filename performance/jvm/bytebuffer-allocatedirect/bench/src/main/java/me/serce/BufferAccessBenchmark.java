package me.serce;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

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
import static java.nio.file.StandardOpenOption.WRITE;

@Fork(1)
@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 1, timeUnit = TimeUnit.MILLISECONDS)
@Measurement(iterations = 3, timeUnit = TimeUnit.MILLISECONDS)
public class BufferAccessBenchmark {

  public static final int SIZE = 32 * 1024 * 1024;

  @Param({
      "direct",
      "direct-native",
      "heap"
  })
  String bufferType;
  LongBuffer buffer;
  long val;


  @Setup
  public void setUp() {
    val = ThreadLocalRandom.current().nextLong();
    switch (bufferType) {
      case "direct":
        buffer = ByteBuffer.allocateDirect(SIZE).asLongBuffer();
        break;
      case "direct-native":
        buffer = ByteBuffer.allocateDirect(SIZE).order(ByteOrder.nativeOrder()).asLongBuffer();
        break;
      case "heap":
        buffer = ByteBuffer.allocate(SIZE).asLongBuffer();
        break;
      default:
        throw new AssertionError();
    }
  }

  @Fork(jvmArgsAppend = {
      "-XX:+UnlockDiagnosticVMOptions",
      "-XX:PrintAssemblyOptions=intel",
      "-XX:CompileCommand=print,*BufferAccessBenchmark.putLong*",
  })
  @Benchmark
  public void putLong(Blackhole blackhole) throws Exception {
    long newVal = this.val;
    LongBuffer thisBuf = this.buffer;
    for (int i = 0; i < SIZE / 8; i++) {
      thisBuf.put(i, newVal);
    }
  }
}
