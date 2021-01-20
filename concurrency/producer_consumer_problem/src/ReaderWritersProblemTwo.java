import java.util.concurrent.Semaphore;

public class ReaderWritersProblemTwo {
    static Semaphore readLock = new Semaphore(1);
    static Semaphore writeLock = new Semaphore(1);
    static int readCount = 0;
    static int shared = 0;

    static class Read implements Runnable {

        @Override
        public void run() {
            while (true) {
                try {
                    readLock.acquire();
                    readCount++;
                    if (readCount == 1) {
                        writeLock.acquire();
                    }
                    readLock.release();

                    // Reading Section (Within writeLock because this is critical)
                    System.out.println("Thread "+Thread.currentThread().getName() + " is READING");
                    System.out.println("Read: " + shared);
                    Thread.sleep(1500);
                    System.out.println("Thread "+Thread.currentThread().getName() + " has FINISHED READING");

                    readLock.acquire();
                    readCount--;

                    if (readCount == 0) {
                        writeLock.release();
                    }
                    readLock.release();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    static class Write implements Runnable {
        @Override
        public void run() {
            while (true) {
                try {
                    writeLock.acquire();

                    System.out.println("Writing...");
                    shared += 2;
                    Thread.sleep(100);
                    System.out.println("Finished Writing");
                    writeLock.release();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Read read = new Read();
        Write write = new Write();
        Thread t1 = new Thread(read);
        t1.setName("thread1");
        Thread t2 = new Thread(read);
        t2.setName("thread2");
        Thread t3 = new Thread(write);
        t3.setName("thread3");
        Thread t4 = new Thread(read);
        t4.setName("thread4");
        t1.start();
        t3.start();
        t2.start();
        t4.start();
    }
}
