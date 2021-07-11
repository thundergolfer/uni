public class Tuple {
    private Item[] tupleItems;

    public Tuple(String[] items, TupleDesc<String> desc) {
        this.tupleItems = new Item[desc.size()];

        for (int i = 0; i < items.length; i++) {
            String itemType = desc.get(i);

            if (itemType.equals("TEXT")) {
                tupleItems[i] = new StringItem(items[i]);
            } else if (itemType.equals("LONG")) {
                long val = Long.parseLong(items[i]);
                tupleItems[i] = new LongItem(val);
            } else { // item type is  "INT"
                int val = Integer.parseInt(items[i]);
                tupleItems[i] = new IntItem(val);
            }
        }
    }

    public Tuple(Item[] items) {
        this.tupleItems = items;
    }

    public int length() {
        int total = 0;

        for (int i = 0; i < tupleItems.length; i++) {
            if (tupleItems[i] != null) {
                total += tupleItems[i].length();
            }
            total += 1; // space for delimiter
        }
        return total;
    }

    public Item[] getItems() {
        return tupleItems;
    }

    public Item getItem(int index) {
        return tupleItems[index];
    }

    public String toString() {
        StringBuilder builder = new StringBuilder();
        for (Item i : tupleItems) {
            if (i != null) {
                builder.append(i.toString());
            }
            builder.append(" | ");
        }
        return builder.toString();
    }
}
