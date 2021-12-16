package data_structures;

// TODO(Jonathon): Should support min/max versions.
public class Heap {
    private int[] heap;
    private int size;
    private int maxSize;

    public Heap(int maxSize) {
        this.maxSize = maxSize;
        this.size = 0;
        this.heap = new int[this.maxSize];
    }

    private int parent(int pos) {
        return (pos -1) / 2;
    }

    private int kthChild(int i, int k){
        return 2*i+k;
    }

    private void swap(int first, int second) {
        int tmp;
        tmp = this.heap[first];
        this.heap[first] = this.heap[second];
        this.heap[second] = tmp;
    }

    /**
     *  This will insert new element in to heap
     *  Complexity: O(log N)
     *  In the worst case scenario, it needs to traverse until the root.
     */
    public void insert(int item) {
        if (this.size == this.maxSize) {
            throw new RuntimeException("Cannot insert. Heap is at max size.");
        }

        // Initially insert at end.
        this.heap[this.size] = item;

        for(int curr = this.size; this.heap[curr] > this.heap[parent(curr)]; curr = parent(curr)) {
            swap(curr, parent(curr));
        }
        this.size++;
        return;
    }

    private boolean isLeaf(int pos) {
        if (pos > (size / 2) && pos <= size) {
            return true;
        }
        return false;
    }

    public int pop() {
        if (this.isEmpty()) {
            throw new RuntimeException("Cannot pop from empty heap.");
        }

        int popped = this.heap[0];
        this.heap[0] = this.heap[--this.size];  // Move last element to root.

//        for (int curr = 0; this.heap[curr] < this.heap[kthChild(curr, 1)])
        int curr = 0;

        while (!isLeaf(curr)) {
            if (
                    this.heap[curr] < this.heap[kthChild(curr, 1)]
                    || this.heap[curr] < this.heap[kthChild(curr, 2)]
            ) {
                if (this.heap[kthChild(curr, 1)] > this.heap[kthChild(curr, 2)]) {
                    swap(curr, kthChild(curr, 1));
                    curr = kthChild(curr, 1);
                } else {
                    swap(curr, kthChild(curr, 2));
                    curr = kthChild(curr, 2);
                }
            } else {
                break;
            }
        }
        return popped;
    }

    public boolean isEmpty() {
        return this.size == 0;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < size; i++) {
            sb.append(this.heap[i]);
            sb.append(", ");
        }
        return sb.toString();
    }

    public static void main(String[] arg) {
        // Display message for better readability
        System.out.println("The Max Heap is ");

        Heap maxHeap = new Heap(15);

        maxHeap.insert(5);
        maxHeap.insert(3);
        maxHeap.insert(17);
        maxHeap.insert(10);
        maxHeap.insert(84);
        maxHeap.insert(19);
        maxHeap.insert(6);
        maxHeap.insert(22);
        maxHeap.insert(9);

        System.out.println(maxHeap.toString());

        StringBuilder sb = new StringBuilder();
        while (!maxHeap.isEmpty()) {
            sb.append(maxHeap.pop());
            sb.append(", ");
        }
        System.out.println(sb.toString());

        // Print and display the maximum value in heap
//        System.out.println("The max val is " + maxHeap.extractMax());
    }


}
