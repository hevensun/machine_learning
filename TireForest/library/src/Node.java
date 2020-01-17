import java.util.HashMap;

/**
 * Created by slade on 2019/12/30.
 */
public class Node {
    private HashMap<Character, Node> children;
    private boolean isWord;

    public Node(boolean isWord) {
        this.isWord = isWord;
        this.children = new HashMap<Character, Node>();
    }

    public Node() {
        this(false);
    }

    public HashMap<Character, Node> getChildren() {
        return children;
    }

    public void setChildren(HashMap<Character, Node> children) {
        this.children = children;
    }

    public boolean isWord() {
        return isWord;
    }

    public void setWord(boolean word) {
        isWord = word;
    }
}
