package atomicStuff;

/**
 * Run the main method of this class and you will see Runners in different threads get the same value
 */
public class UnsafeCounter {
    private int count;

    public int increment() {
        return ++count;
    }


    public static void main(String[] args) {
        UnsafeCounter counter = new UnsafeCounter();

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
}

