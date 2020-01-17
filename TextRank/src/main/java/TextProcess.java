import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by slade on 2019/12/29.
 */
public class TextProcess {
    static List<String> splitDocument(String document) {
        List<String> sentence = new ArrayList<>();
        if (document == null) {
            return sentence;
        }
        for (String doc : document.split("[\n]")) {
            doc = doc.trim();
            if (doc.length() == 0) {
                continue;
            }
            for (String s : doc.split("[，,。:：“”？?！!；;]")) {
                s = s.trim();
                if (s.length() == 0) continue;
                sentence.add(s);
            }
        }
        return sentence;
    }

    static List<List<String>> splitDocumentList(String document) {
        List<String> sentenceList = splitDocument(document);
        List<List<String>> docs = new ArrayList<List<String>>();

        for (String sentence : sentenceList
                ) {
            List<Term> termList = HanLP.segment(sentence);
            List<String> wordList = new LinkedList<>();
            for (Term term : termList) {
                wordList.add(term.word);
            }
            docs.add(wordList);
        }

        return docs;
    }
}
