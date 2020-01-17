/**
 * Created by slade on 2019/12/30.
 */
public class Tire {
    Node root;
    private int size;

    public Tire() {
        root = new Node();
        size = 0;
    }

    public int getSize() {
        return size;
    }

    public void insert(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            if (cur.getChildren().get(c) == null) {
                Node temp = new Node();
                cur.getChildren().put(c, temp);
            }
            cur = cur.getChildren().get(c);
        }

        if (!cur.isWord()) {
            ++size;
            cur.setWord(true);
        }
    }

    public boolean contains(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            char temp = word.charAt(i);
            if (!cur.getChildren().containsKey(temp)) {
                return false;
            }
            cur = cur.getChildren().get(temp);
        }
        return cur.isWord();
    }

    public boolean isPrefix(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            if (!cur.getChildren().containsKey(c)) return false;
            cur = cur.getChildren().get(c);
        }
        return true;
    }
}
