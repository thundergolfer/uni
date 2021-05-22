package me.serce;

import org.openjdk.jmh.annotations.*;

import java.nio.ByteBuffer;
import java.util.concurrent.TimeUnit;

@Fork(1)
@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, timeUnit = TimeUnit.MICROSECONDS)
@Measurement(iterations = 5, timeUnit = TimeUnit.MILLISECONDS)
public class AllocateBuffer1 {
  @Param({"128", "1024", "16384"}) int size;

  @Benchmark
  public ByteBuffer heap() {
    return ByteBuffer.allocate(size);
  }

  @Benchmark
  public ByteBuffer direct() {
    return ByteBuffer.allocateDirect(size);
  }
}
