package atomicStuff;

import java.util.concurrent.

public class SafeCounter {
    private volatile int count;

    /**
     * merely using volatile is not suitable for a read-update-write operation.
     * we could miss an update
     * @return
     */
    public int unsafeIncrement() {
        return ++count;
    }

    /**
     * With synchronized, only one thread can enter the method at a time.
     * We still need to have "volatile" on the count variable, as we need to guarantee we
     * see the latest value of it, and not a thread-cached version
     * @return
     */
    public synchronized int increment() {
        return ++count;
    }

    public static void runUnsafeIncrement(SafeCounter counter) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("Runner got: " + counter.unsafeIncrement());
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("Runner got: " + counter.unsafeIncrement());
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("Runner got: " + counter.unsafeIncrement());
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    public static void runSafeIncrement(SafeCounter counter) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("Runner got: " + counter.increment());
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("Runner got: " + counter.increment());
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        System.out.println("Runner got: " + counter.increment());
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    public static void main(String[] args) {
        SafeCounter counter = new SafeCounter();

        runSafeIncrement(counter);
    }
}
