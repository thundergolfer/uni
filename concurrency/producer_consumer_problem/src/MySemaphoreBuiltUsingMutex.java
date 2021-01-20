import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class MySemaphoreBuiltUsingMutex {
    Lock mutex;
    Lock valueMutex;
    int capacity;
    String name;

    public MySemaphoreBuiltUsingMutex(int capacity, String name) {
        this.name = name;
        this.capacity = capacity;
        this.mutex = new ReentrantLock();
        this.valueMutex = new ReentrantLock();
    }

    public synchronized void acquire() throws InterruptedException {
        while (true) {
            valueMutex.lock();

            if (this.capacity == 0) {
                valueMutex.unlock();
                wait();
                continue;
            }

            this.capacity--;
            valueMutex.unlock();
            break;
        }
        notify();
    }

    public synchronized void release() {
        valueMutex.lock();
        this.capacity++;
        valueMutex.unlock();
        notify();
    }
}
