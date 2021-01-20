import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReadersWritersProblemWithJavaPackageClass {
    int numReaders;
    ReadWriteLock rwLock;
    int sharedResource;

    public ReadersWritersProblemWithJavaPackageClass(int numReaders) {
        this.numReaders = numReaders;
        this.rwLock = new ReentrantReadWriteLock(true);
    }

    public void runProblem() {
        String[] readerNames = {
                "A",
                "B",
                "C",
                "D",
                "E",
                "F"
        };
        Reader[] readers = new Reader[numReaders];
        for (int i = 0; i < this.numReaders; i++) {
            readers[i] = new Reader(readerNames[i]);
            new Thread(readers[i]).start();;
        }

        new Thread(new Writer("WRITER")).start();
//        new Thread(new Writer("WRITER 2")).start();
    }

    class Reader implements Runnable {
        String name;

        Reader(String name) {
            this.name = name;
        }


        @Override
        public void run(){
            while (true) {
                rwLock.readLock().lock();

                int blah = sharedResource;

                System.out.format("Reader '%s' read %d\n", this.name, blah);

                rwLock.readLock().unlock();

                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    class Writer implements Runnable {
        String name;

        Writer(String name) {
            this.name = name;
        }

        @Override
        public void run() {
            while (true) {
                rwLock.writeLock().lock();

                sharedResource += 1;

                System.out.format("Writer '%s' changed shared resource to: %d\n", this.name, sharedResource);

                rwLock.writeLock().unlock();

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) {
        ReadersWritersProblemWithJavaPackageClass problem = new ReadersWritersProblemWithJavaPackageClass(5);

        problem.runProblem();
    }
}
