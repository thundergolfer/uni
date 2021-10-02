package algorithms.named;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class LinkedList<T> {
    static class Node<T> {
        T data;
        public Node<T> next;

        Node(T data) {
            this.data = data;
        }
    }

    Node<T> head;
    Node<T> tail;

    public LinkedList() {
        this.head = null;
    }

    void add(T elem) {
        Node<T> n = new Node<>(elem);
        if (this.head == null) {
            this.head = n;
        } else {
            Node<T> curr;
            for (curr = this.head; curr.next != null; curr = curr.next) {}
            curr.next = n;
        }
    }

    void reverse() {
        // TODO(Jonathon)
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Node<T> curr = this.head; curr != null; curr = curr.next) {
            sb.append(curr.data);
            if (curr.next != null) {
                sb.append(" -> ");
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println("Hello world");
        System.exit(0);
    }

    @Test
    public void testToString() {
        assertEquals("", new LinkedList<>().toString());
        LinkedList<Integer> ll = new LinkedList<>();
        ll.add(1);
        ll.add(2);
        ll.add(3);
        assertEquals("1 -> 2 -> 3", ll.toString());
    }
}
