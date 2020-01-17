import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary;
import com.hankcs.hanlp.seg.common.Term;

import java.util.*;

public class TextRankKeyWord {
    public final int nKeyWords = 3;

    /*阻尼系数*/
    public float d = 0.85f;

    public final int maxIter = 500;
    public final float minDiff = 0.01f;
    public final int windowSize = 5;

    public TextRankKeyWord() {
    }

    public String getKeyWord(String title, String content) {
        List<Term> termList = HanLP.segment(title + content);
        System.out.println(termList);
        List<String> wordList = new ArrayList<>();
        for (Term term : termList
        ) {
            if (isInclude(term)) wordList.add(term.word);
        }
        System.out.println(wordList);
        Map<String, Set<String>> words = new HashMap<>();
        Queue<String> queue = new LinkedList<String>();

        for (String w : wordList
        ) {
            if (!words.containsKey(w)) {
                words.put(w, new HashSet<String>());
            }
            queue.add(w);

            /*windows size*/
            if (queue.size() > windowSize) {
                queue.poll();
            }
            for (String word1 : queue
            ) {
                for (String word2 : queue
                ) {
                    if (word1.equals(word2)) {
                        continue;
                    }
                    /*word1和word2之间相关联*/
                    words.get(word1).add(word2);
                    words.get(word2).add(word1);
                }
            }
        }

        Map<String, Float> score = new HashMap<String, Float>();
        for (int i = 0; i < maxIter; i++) {
            /*每次更新，都需要重置初始化参数*/
            Map<String, Float> m = new HashMap<>();
            float maxDiff = 0;
            for (Map.Entry<String, Set<String>> entry : words.entrySet()
            ) {
                String key = entry.getKey();
                Set<String> value = entry.getValue();

                /*初始化1-d,一般为0.15*/
                m.put(key, 1 - d);

                for (String match : value
                ) {
                    int size = words.get(match).size();
                    if (key == match || size == 0) continue;

                    /*更新m的系数*/
                    m.put(key, m.get(key) + d / size * (score.get(match) == null ? 0 : score.get(match)));
                }

                /*如果key在更新列表里面的话，计算提升度，否则更新为0*/
                maxDiff = Math.max(maxDiff, Math.abs(m.get(key) - (score.get(key) == null ? 0 : score.get(key))));
            }
            /*更新全局参数不同词的权重*/
            score = m;
            if (maxDiff < minDiff) break;
        }
        List<Map.Entry<String, Float>> entryList = new ArrayList<>(score.entrySet());
        System.out.println(entryList);
        Collections.sort(entryList, new Comparator<Map.Entry<String, Float>>() {
            @Override
            public int compare(Map.Entry<String, Float> o1, Map.Entry<String, Float> o2) {
                return o1.getValue() - o2.getValue() > 0 ? -1 : 1;
            }
        });
        String res = "";
        for (int j = 0; j < nKeyWords; j++) {
            res += entryList.get(j).getKey() + "----";
        }
        return res;
    }

    public Boolean isInclude(Term term) {
        return CoreStopWordDictionary.shouldInclude(term);
    }

    public static void main(String[] args) {
        String content = "有种说法是：“未来AI将取代大部分主要依靠左脑思维完成的工作。”，当然也包括记忆力。人脑以后真的比不上“计算机”了 吗？生活在未来与人工智能并存的时代，孩子的大脑要怎么开发？孩子的记忆力培养还重要吗？";
        System.out.println(new TextRankKeyWord().getKeyWord("", content));
    }
}
