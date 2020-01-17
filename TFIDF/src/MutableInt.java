/**
 * Created by slade on 2019/12/27.
 */
public class MutableInt {
    private int counter = 1;

    public MutableInt() {
    }

    static MutableInt createMutableInt() {
        return new MutableInt();
    }

    public void increaseCounter() {
        this.counter++;
    }

    @Override
    public String toString() {
        return "MutableInt{" +
                "counter=" + counter +
                '}';
    }

    public int getCounter() {
        return counter;
    }

    public void setCounter(int counter) {
        this.counter = counter;
    }
}
