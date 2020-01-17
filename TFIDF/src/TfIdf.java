import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by slade on 2019/12/27.
 */
public class TfIdf {
    private int N;
    private final List<String> documents;

    public TfIdf(List<String> documents) {
        this.documents = documents;
    }

    public List<String> getDocuments() {
        return documents;
    }

    List<String> buildWords(String document) {
        List<String> wordList = new ArrayList<>();
        Matcher matcher = Pattern.compile("[a-zA-Z]+").matcher(document);
        while (matcher.find()) {
            wordList.add(matcher.group());
        }
        return wordList;
    }

    public List<Map<String, MutableInt>> tf() {
        List<Map<String, MutableInt>> list = new ArrayList<>();

        for (String docment : documents
                ) {
            Map<String, MutableInt> map = new HashMap<>();
            List<String> words = buildWords(docment);
            for (String word : words) {
                MutableInt counter = map.get(word);
                if (counter == null) {
                    map.put(word, MutableInt.createMutableInt());
                } else {
                    counter.increaseCounter();
                }
            }
            list.add(map);
        }
        return list;
    }


    public Map<String, MutableInt> idf() {
        HashMap<String, MutableInt> map = new HashMap<>();
        List<String> list;
        Set<String> set;
        for (String docment : documents
                ) {
            N++;
            list = buildWords(docment);
            set = new HashSet<>(list);
            for (String word : set
                    ) {
                MutableInt counter = map.get(word);
                if (counter == null) {
                    map.put(word, MutableInt.createMutableInt());
                } else {
                    counter.increaseCounter();
                }
            }
            list.clear();
            set.clear();
        }
        return map;
    }

    public List<Map<String, Double>> tfidf() {
        List<Map<String, MutableInt>> list = tf();
        Map<String, MutableInt> map = idf();

        List<Map<String, Double>> list1 = new ArrayList<>();

        for (Map<String, MutableInt> m : list
                ) {
            int docment_word = 0;
            for (String word : m.keySet()
                    ) {
                docment_word += m.get(word).getCounter();
            }

            Map<String, Double> map1 = new HashMap<>();
            for (String s : m.keySet()
                    ) {
                MutableInt word = m.get(s);

                double score = (double) word.getCounter() / docment_word * Math.log(N / (map.get(s).getCounter() + 1e-100));
                map1.put(s, score);
            }
            list1.add(map1);
        }
        return list1;
    }
}