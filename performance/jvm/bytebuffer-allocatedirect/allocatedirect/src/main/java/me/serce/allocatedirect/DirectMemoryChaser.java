package me.serce.allocatedirect;

import java.nio.ByteBuffer;

public class DirectMemoryChaser {
  public static void main(String[] args) {
    while (true) {
      ByteBuffer.allocateDirect(1024);
    }
  }
}
