import java.util.concurrent.LinkedBlockingQueue;

public class ProducerConsumerWithConcurrentPackage {
    LinkedBlockingQueue<Integer> q;
    int capacity;

    public ProducerConsumerWithConcurrentPackage(int capacity) {
        this.capacity = capacity;
        this.q = new LinkedBlockingQueue<>(capacity);
    }

    public void produce() throws InterruptedException {
        int value = 0;

        while (true) {
            System.out.println("Producer added to queue: " + value);
            this.q.offer(value++);
            Thread.sleep(1000);
        }
    }

    public void consume() throws InterruptedException {
        while (true) {
            int x = this.q.take();

            System.out.println("Consumer consumed: " + x);
            Thread.sleep(1000);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        int capacity = 5;
        ProducerConsumerWithConcurrentPackage pc = new ProducerConsumerWithConcurrentPackage(capacity);

        Thread one = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.consume();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        Thread two = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.produce();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        one.start();
        two.start();

        one.join();
        two.join();
    }
}
