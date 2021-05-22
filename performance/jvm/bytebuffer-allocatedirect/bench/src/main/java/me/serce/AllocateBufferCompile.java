package me.serce;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.nio.ByteBuffer;
import java.util.concurrent.TimeUnit;

@Fork(1)
@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, timeUnit = TimeUnit.MICROSECONDS)
@Measurement(iterations = 5, timeUnit = TimeUnit.MILLISECONDS)
public class AllocateBufferCompile {
  @Param({"128"}) int size;

  @Fork(jvmArgsAppend = {
    "-XX:+UnlockDiagnosticVMOptions",
    "-XX:PrintAssemblyOptions=intel",
    "-XX:CompileCommand=print,*AllocateBuffer2.heap*",
  })
  @Benchmark
  public ByteBuffer heap() {
    return ByteBuffer.allocate(size);
  }

  @Fork(jvmArgsAppend = {
      "-XX:+UnlockDiagnosticVMOptions",
      "-XX:PrintAssemblyOptions=intel",
      "-XX:CompileCommand=print,*AllocateBuffer2.direct*",
      "-XX:CompileCommand=print,*DirectByteBuffer.*",
  })
  @Benchmark
  public ByteBuffer direct() {
    return ByteBuffer.allocateDirect(size);
  }

  @Benchmark
  public void combined(Blackhole blackhole) {
    blackhole.consume(ByteBuffer.allocate(size));
    blackhole.consume(ByteBuffer.allocateDirect(size));
  }
}
