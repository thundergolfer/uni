import java.util.concurrent.Semaphore;

public class ReadersWritersProblem {
    int sharedResource;
    int numReaders;

    Semaphore readersSemaphore;
    Semaphore writersSemaphore;

    public ReadersWritersProblem(int numReaders) {
        this.numReaders = numReaders;
        this.writersSemaphore = new Semaphore(1);
        this.readersSemaphore = new Semaphore(numReaders);
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

        new Thread(new Writer("WRITER", numReaders)).start();
        new Thread(new Writer("WRITER 2", numReaders)).start();
    }


    class Reader implements Runnable {
        String name;

        Reader(String name) {
            this.name = name;
        }

        public void read() throws InterruptedException {
            while (true) {
                readersSemaphore.acquire();
                int shared = sharedResource;
                System.out.println("Reader got: " + shared);

                readersSemaphore.release();

                Thread.sleep(1000); // for readability
            }
        }

        @Override
        public void run() {
            try {
                read();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    class Writer implements Runnable {
        String name;
        int numReaders;

        Writer(String name, int numReaders) {
            this.name = name;
            this.numReaders = numReaders;
        }

        public void write() throws InterruptedException {
            int value = 0;

            while (true) {
                writersSemaphore.acquire();
                for (int i = 0; i < this.numReaders; i++) {
                    readersSemaphore.acquire();
                }

                sharedResource += 2;

                System.out.println(name + ": Shared resource is now: " + sharedResource);

                for (int i = 0; i < this.numReaders; i++) {
                    readersSemaphore.release();
                }
                writersSemaphore.release();
                Thread.sleep(1000); // for program understandability
            }
        }

        @Override
        public void run() {
            try {
                write();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        ReadersWritersProblem problem = new ReadersWritersProblem(5);
        problem.runProblem();
    }

}
