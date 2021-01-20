import java.util.LinkedList;

public class ProducerConsumerWithMutexBasedSemaphore {
    int capacity;
    MySemaphoreBuiltUsingMutex fillCount;
    MySemaphoreBuiltUsingMutex emptyCount;
    LinkedList<Integer> list;


    public ProducerConsumerWithMutexBasedSemaphore(int capacity) {
        this.capacity = capacity;
        this.fillCount = new MySemaphoreBuiltUsingMutex(0, "fillCount");
        this.emptyCount = new MySemaphoreBuiltUsingMutex(capacity, "emptyCount");
        this.list = new LinkedList<>();
    }

    public void produce(String name) throws InterruptedException {
        int value = 0;

        while (true) {
            emptyCount.acquire();

            System.out.println("Producer '" + name + "' producing: " + value);
            list.add(value++);

            fillCount.release();

            Thread.sleep(1000); // for better understandability
        }
    }

    public void consume(String name) throws InterruptedException {
        while (true) {
            fillCount.acquire();

            int consumed = list.removeFirst();

            System.out.println("Consumer '" + name + "'consumed: " + consumed);

            emptyCount.release();

            Thread.sleep(1000); // for better understandability
        }
    }

    public static void main(String[] args) throws InterruptedException {
        int capacity = 5;
        ProducerConsumerWithMutexBasedSemaphore pc = new ProducerConsumerWithMutexBasedSemaphore(capacity);

        Thread one = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.consume("Jane");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        Thread two = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.produce("John");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        Thread three = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.consume("Cecil");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        one.start();
        two.start();
        three.start();

        one.join();
        two.join();
        three.join();
    }
}
