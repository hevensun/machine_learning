import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary;
import com.hankcs.hanlp.seg.common.Term;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by slade on 2020/1/4.
 */


public class Rake {
    private String doc;
    private Article article;
    private int min_word_return_size = 2;
    private int max_freq = 5;
    private float top_x = 0.3f;
    private Pattern pattern = Pattern.compile("[^\u4e00-\u9fa5A-Za-z0-9,.!?，。？！；;~～……、]");
    private Pattern patternSplit = Pattern.compile("[',', '.', '?', '!', '~', ';', '，', '。', '？', '！', '～', '；', '……', '、']");

    public Rake(String doc) {
        this.doc = doc;
        this.article = new Article(doc);
    }

    public Rake(String doc, int min_word_return_size, int max_freq, float top_x) {
        this.doc = doc;
        this.article = new Article(doc, min_word_return_size, max_freq, top_x);
    }

    public List<String> separateSentence() {
        Matcher matcher = pattern.matcher(doc);
        String replaceText = matcher.replaceAll("");
        String[] textList = replaceText.split("[,| .| ?| !| ~| ;| ，| 。| ？| ！| ～| ；| ……| 、]");
        List<String> res = new ArrayList<String>();
        for (String sentence : textList
        ) {
            if (sentence.length() >= this.article.getMin_word_return_size() && !Utils.isNumber(sentence)) {
                res.add(sentence);
            }
        }
        return res;
    }

    public List<String> separateWord(String sentence) {
        List<Term> termList = HanLP.segment(sentence);
        List<String> res = new ArrayList<String>();
        for (Term term : termList
        ) {
            if (isInclude(term) && term.word.length() >= this.article.getMin_word_return_size() && !Utils.isNumber(term.word)) {
                res.add(term.word);
            }
        }
        return res;
    }

    private boolean isInclude(Term term) {
        return CoreStopWordDictionary.shouldInclude(term);
    }

    public HashMap<String, Float> calculateWordScore(List<String> phraseList) {
        HashMap<String, Float> wordFrequency = new HashMap<String, Float>();
        HashMap<String, Float> wordDegree = new HashMap<String, Float>();
        for (String item : phraseList
        ) {
            List<String> wordList = separateWord(item);
            int wordListLength = wordList.size();
            int wordListDegree = Math.max(wordListLength - 1, 0);

            int wordListDegreeReshape = Math.min(wordListDegree, article.getMax_freq());

            /*更新每段的词频+度*/
            for (String word : wordList
            ) {
                wordFrequency.put(word, wordFrequency.get(word) == null ? 1 : wordFrequency.get(word) + 1);
                wordDegree.put(word, wordDegree.get(word) == null ? wordListDegreeReshape : wordDegree.get(word) + wordListDegreeReshape);
            }
        }

        /*修正完整的度*/
        for (String w : wordFrequency.keySet()
        ) {
            wordDegree.put(w, wordDegree.get(w) + wordFrequency.get(w));
        }

        /*计算度得分*/
        HashMap<String, Float> score = new HashMap<String, Float>();

        for (String s : wordFrequency.keySet()
        ) {
            score.put(s, wordFrequency.get(s) == 0 ? 0 : wordDegree.get(s) / wordFrequency.get(s));
        }
        return score;
    }

    public List generateCandidateKeywords(List<String> phraseList) {
        HashMap<String, Float> keywords = new HashMap<String, Float>();

        HashMap<String, Float> scores = calculateWordScore(phraseList);
        for (String item : phraseList
        ) {
            List<String> list = separateWord(item);
            float candidateScore = 0f;
            if (list.size() == 0) {
                continue;
            }
            for (String word : list
            ) {
                candidateScore += scores.get(word);
            }
            /*长度平衡*/
            keywords.put(item, candidateScore / list.size());
        }
        List<Map.Entry<String, Float>> keywordsList = new ArrayList<Map.Entry<String, Float>>(keywords.entrySet());
        Collections.sort(keywordsList, new Comparator<Map.Entry<String, Float>>() {
            public int compare(Map.Entry<String, Float> o1, Map.Entry<String, Float> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });
        return keywordsList;
    }
}
