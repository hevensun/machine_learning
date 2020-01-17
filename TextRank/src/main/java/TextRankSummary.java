import java.util.*;

public class TextRankSummary {
    /*阻尼系数*/
    private double d = 0.85;

    private int maxIter = 500;
    private double stopDiff = 0.01;

    /*文档数*/
    private int D = -1;

    /*input*/
    List<List<String>> docs = new ArrayList<>();

    /*output*/
    private Map<Double, Integer> scores = new TreeMap<Double, Integer>(Collections.reverseOrder());

    /*nxn转移矩阵*/
    private Double[][] weight;

    /*1xn转移矩阵*/
    private Double[] weight_cbind;

    /*收敛值*/
    private Double[] res;

    BM25 bm25;

    public TextRankSummary(List<List<String>> docs) {
        this.docs = docs;
        bm25 = new BM25(docs);
        D = docs.size();
        weight = new Double[D][D];
        weight_cbind = new Double[D];
        res = new Double[D];
        init();
    }

    public void init() {
        int cnt = 0;
        for (List<String> doc : docs) {
            List<Double> similarities = bm25.simAll(doc);
            similarities.toArray(weight[cnt]);
            /*剔除自己外，所有的得分和*/
            weight_cbind[cnt] = sum(similarities) - similarities.get(cnt);
            /*初始化权重*/
            res[cnt] = 1.0;
            ++cnt;
        }


        /*迭代开始*/
        for (int i = 0; i < maxIter; i++) {
            Double[] m = new Double[D];
            Double maxdiff = 0.0;
            /*文本遍历*/
            for (int j = 0; j < D; j++) {
                m[j] = 1 - d;
                for (int k = 0; k < D; k++) {
                    if (j == k || weight_cbind[k] == 0) continue;
                    m[j] += (d * weight[k][j] / weight_cbind[k] * res[k]);

                    double diff = Math.abs(m[j] - res[j]);
                    maxdiff = Math.max(maxdiff, diff);
                }
            }
            res = m;
            if (maxdiff <= stopDiff) break;
        }

        /*权重排序*/
        for (int i = 0; i < D; i++) {
            scores.put(res[i], i);
        }
    }

    public static double sum(List<Double> list) {
        Double total = 0.0;
        for (int i = 0; i < list.size(); i++) {
            total += list.get(i);
        }
        return total;
    }

    public int[] getTopSentence(int size) {
        Collection<Integer> values = scores.values();
        size = Math.min(size, scores.size());
        int[] ans = new int[size];
        int cnt = 0;
        Iterator<Integer> iterator = values.iterator();
        while (cnt < size) {
            ans[cnt] = iterator.next();
            ++cnt;
        }
        return ans;
    }
}
