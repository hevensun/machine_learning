import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import com.alibaba.fastjson.JSON;
/**
 * Created by slade on 2020/1/4.
 */
public class Test {
    public static void main(String[] args) {
        String text = "如何在一段文本之中提取出相应的关键词呢？\n" +
                "之前我有想过用机器学习的<方法>来进行词法分析，18米,但是在项目中测试时正确率不够。于是这时候便有了 HanLP-汉语言处理包 来进行提取关键词的想法。";
        Rake rake = new Rake(text);
        List<String> l = rake.separateSentence();

        for (String item : l
        ) {
            System.out.println(item);
            System.out.println(rake.separateWord(item));
        }

        System.out.println(rake.generateCandidateKeywords(l));


        String jsonString = JSON.toJSONString(new Article("asdw"));
        System.out.println(jsonString);
    }
}
