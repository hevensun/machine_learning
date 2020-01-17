import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by slade on 2019/12/28.
 */
public class BM25 {
    /*样本*/
    List<List<String>> docs;
    /*句子数*/
    private int D;
    /*平均句子长度*/
    private double avgdl;
    /*每个文档中每个词的出现次数*/
    private ArrayList<Map<String, Integer>> f = new ArrayList<>();
    /*每个词出现的文档数*/
    private Map<String, Integer> df = new HashMap<>();
    private Map<String, Double> idf = new HashMap<>();
    private double k1 = 1.5;
    private double b = 0.75;

    public Map<String, Integer> getDf() {
        return df;
    }

    public Map<String, Double> getIdf() {
        return idf;
    }

    public int getD() {
        return D;
    }

    public double getAvgdl() {
        return avgdl;
    }

    public ArrayList<Map<String, Integer>> getF() {
        return f;
    }

    public BM25(List<List<String>> docs) {

        this.docs = docs;
        D = docs.size();

        for (List<String> doc : docs) {
            avgdl += doc.size();
            Map<String, Integer> tmp = new HashMap<>();
            for (String word : doc
                    ) {
                Integer freq = tmp.get(word);
                freq = (freq == null ? 0 : freq) + 1;
                tmp.put(word, freq);
            }
            f.add(tmp);

            for (Map.Entry<String, Integer> pair : tmp.entrySet()
                    ) {
                String word = pair.getKey();
                Integer freq = df.get(word);
                freq = (freq == null ? 0 : freq) + 1;
                df.put(word, freq);
            }

            for (Map.Entry<String, Integer> pair : df.entrySet()
                    ) {
                String word = pair.getKey();
                Integer freq = pair.getValue();
                idf.put(word, Math.log(D - freq + 0.5) - Math.log(0.5 + freq));
            }
        }
        avgdl /= D;
    }

    public double sim(List<String> doc, Integer index) {
        double score = 0;
        for (String word : doc
                ) {
            if (!f.get(index).containsKey(word)) continue;
            int size = docs.get(index).size();
            Integer wf = f.get(index).get(word);
            score += (idf.get(word) * wf * (k1 + 1)
                    / (wf + k1 * (1 - b + b * size
                    / avgdl)));
        }
        return score;
    }

    public List simAll(List<String> doc) {
        List scores = new ArrayList<>();
        Double score;
        for (int i = 0; i < D; i++) {
            score = sim(doc, i);
            scores.add(score);
        }
        return scores;
    }
}
