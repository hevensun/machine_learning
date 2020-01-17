import java.util.ArrayList;
import java.util.List;

/**
 * Created by slade on 2019/12/28.
 */
public class Main {
    public static void main(String[] args) {
        ArrayList<List<String>> docs = new ArrayList<>();
        List<String> doc = new ArrayList<>();
        doc.add("i");
        doc.add("am");
        doc.add("jack");

        List<String> doc1 = new ArrayList<>();
        doc1.add("u");
        doc1.add("are");
        doc1.add("jack");

        docs.add(doc);
        docs.add(doc1);

        BM25 bm25 = new BM25(docs);
        System.out.println(bm25.simAll(doc));
    }
}
