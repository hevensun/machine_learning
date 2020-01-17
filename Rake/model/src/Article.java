/**
 * Created by slade on 2020/1/4.
 */
public class Article {
    private String doc;
    private int min_word_return_size = 2;
    private int max_freq = 5;
    private float top_x = 0.3f;

    public Article(String doc) {
        this.doc = doc;
    }

    public Article(String doc, int min_word_return_size, int max_freq, float top_x) {
        this.doc = doc;
        this.min_word_return_size = min_word_return_size;
        this.max_freq = max_freq;
        this.top_x = top_x;
    }

    public int getMin_word_return_size() {
        return min_word_return_size;
    }

    public void setMin_word_return_size(int min_word_return_size) {
        this.min_word_return_size = min_word_return_size;
    }

    public int getMax_freq() {
        return max_freq;
    }

    public void setMax_freq(int max_freq) {
        this.max_freq = max_freq;
    }

    public float getTop_x() {
        return top_x;
    }

    public void setTop_x(float top_x) {
        this.top_x = top_x;
    }
}
