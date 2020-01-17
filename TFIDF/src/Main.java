import java.util.ArrayList;
import java.util.List;

/**
 * Created by slade on 2019/12/27.
 */
public class Main {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("this is china");
        list.add("this is usa");
        list.add("this is is tokyo usa");
        TfIdf tfIdf = new TfIdf(list);
        System.out.println(tfIdf.tfidf());
    }
}
