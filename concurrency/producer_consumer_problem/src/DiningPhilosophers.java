import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Semaphore;

public class DiningPhilosophers {
    int numPhils = 5;
    Semaphore[] forks;

    public DiningPhilosophers() {
        this.forks = new Semaphore[numPhils];
        for (int i = 0; i < numPhils; i++) {
            this.forks[i] = new Semaphore(1);
        }
    }

    public void runProblem() {
        String[] names = {
            "Plato", "Heidegger", "Socrates", "Nietzsche", "Jonathon"
        };

        List<Thread> threads = new LinkedList<Thread>();
        Thread philosopher;
        for (int i = 0; i < numPhils; i++) {
            philosopher = new Thread(new Philosopher(names[i], i));
            threads.add(philosopher);
        }

        for (Thread t : threads) {
            t.start();
        }
    }

    class Philosopher implements Runnable {
        String name;
        int number;

        Philosopher(String name, int number) {
            this.name = name;
            this.number = number;
        }

        @Override
        public void run() {
            while (true) {
                System.out.println(name + " is thinking");
                Semaphore lower = null; Semaphore higher = null;
                try {
                    lower = getLowerFork();
                    higher = getHigherFork();
                    System.out.println(name + " is eating");

                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }


                if (lower != null) lower.release();
                if (higher != null) higher.release();

                try {
                    Thread.sleep(1000); // for understandability
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            }
        }

        private Semaphore getLowerFork() throws InterruptedException {
            int forkNumber;
            if (this.number + 1 == numPhils) {
                forkNumber = 0;
            } else {
                forkNumber = this.number;
            }
            forks[forkNumber].acquire();
            return forks[forkNumber];
        }

        private Semaphore getHigherFork() throws InterruptedException {
            int forkNumber;
            if (this.number + 1 == numPhils) {
                forkNumber = number;
            } else {
                forkNumber = number + 1;
            }

            forks[forkNumber].acquire();
            return forks[forkNumber];
        }
    }

    public static void main(String[] args) {
        DiningPhilosophers problem = new DiningPhilosophers();

        problem.runProblem();
    }
}
