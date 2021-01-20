package com.thundergolfer.uni.concurrency;

import java.util.LinkedList;

public class ProducerConsumer {

    LinkedList<Integer> list = new LinkedList<>();
    int capacity;

    public ProducerConsumer(int capacity) {
        this.capacity = capacity;
    }

    /**
     * Should not try and remove from empty buffer
     * @return
     */
    public int consume() throws InterruptedException {
        while (true) {
            synchronized (this) {
                while (list.size() == 0) {
                    wait();
                }

                int consumed = list.removeFirst();

                System.out.println("Consumer consumed - " + consumed);

                // Wake up producer
                // gets called on every consumption so when buffer is not
                // nearly full the notification will be thrown away
                notify();

                Thread.sleep(1000); // makes it easier to 'see' the program working
            }
        }
    }

    /**
     * Should not try adding to full buffer
     */
    public void produce() throws InterruptedException {
        int value = 0;

        while (true) {
            synchronized (this) {
                while (list.size() == this.capacity) {
                    wait();
                }

                System.out.println("Producer produced - " + value);

                list.add(value++);

                // buffer now has at least 1 element, so 'wake' consumer if its waiting
                notify();

                Thread.sleep(1000); // makes it easier to 'see' the program working
            }
        }
    }

    public static void main(String[] args) {
	    // write your code here
    }
}
