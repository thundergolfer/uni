package com.thundergolfer.uni.concurrency;

import com.thundergolfer.uni.concurrency.ProducerConsumer;

public class RunProblem {
    public static void main(String[] args) throws InterruptedException {
        final ProducerConsumer pc = new ProducerConsumer(10);

        Thread one = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.produce();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            }
        });

        Thread two = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    pc.consume();
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
