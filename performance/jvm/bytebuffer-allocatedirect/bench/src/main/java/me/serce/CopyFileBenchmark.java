package me.serce;

import org.openjdk.jmh.annotations.*;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.FileChannel;
import java.nio.file.Paths;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;

import static java.nio.file.StandardOpenOption.READ;
import static java.nio.file.StandardOpenOption.WRITE;

@Fork(1)
@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 5, timeUnit = TimeUnit.MILLISECONDS)
@Measurement(iterations = 5, timeUnit = TimeUnit.MILLISECONDS)
public class CopyFileBenchmark {

  public static final int SIZE = 64 * 1024 * 1024;
  public static final String DIR = "/tmp/";

  @Param({"direct", "heap"})
  String bufferType;
  ByteBuffer buffer;


  @Setup
  public void setUp() {
    switch (bufferType) {
      case "direct":
        buffer = ByteBuffer.allocateDirect(SIZE).order(ByteOrder.nativeOrder());
        break;
      case "heap":
        buffer = ByteBuffer.allocate(SIZE);
        break;
      default:
        throw new AssertionError();
    }
  }

  static {
    try (FileOutputStream is1 = new FileOutputStream(DIR + "file1");
         FileOutputStream is2 = new FileOutputStream(DIR + "file2")) {
      byte[] bytes = new byte[SIZE];
      ThreadLocalRandom.current().nextBytes(bytes);
      is1.write(bytes);
      ThreadLocalRandom.current().nextBytes(bytes);
      is2.write(bytes);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

  @Benchmark
  public void copyFiles() throws Exception {
    buffer.clear();
    try (FileChannel channel1 = FileChannel.open(Paths.get(DIR + "file1"), READ);
         FileChannel channel2 = FileChannel.open(Paths.get(DIR + "file2"), WRITE)) {
      while (buffer.hasRemaining()) {
        channel1.read(buffer);
      }
      buffer.flip();
      while (buffer.hasRemaining()) {
        channel2.write(buffer);
      }
    }
  }

  @Benchmark
  public void reverseBytesInFiles() throws Exception {
    ByteBuffer buf = this.buffer;
    buf.clear();
    try (FileChannel channel1 = FileChannel.open(Paths.get(DIR + "file1"), READ);
         FileChannel channel2 = FileChannel.open(Paths.get(DIR + "file2"), WRITE)) {
      while (buf.hasRemaining()) {
        channel1.read(buf);
      }
      buf.put(0, buf.get(SIZE - 1));
      buf.flip();
      while (buf.hasRemaining()) {
        channel2.write(buf);
      }
    }
  }

}
