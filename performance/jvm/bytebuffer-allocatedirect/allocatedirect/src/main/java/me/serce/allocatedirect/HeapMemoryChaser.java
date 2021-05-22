package me.serce.allocatedirect;

import java.nio.ByteBuffer;

public class HeapMemoryChaser {
  public static void main(String[] args) {
    while (true) {
      ByteBuffer.allocate(1024);
    }
  }
}
