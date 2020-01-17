/**
 * Created by slade on 2019/12/30.
 */

public class Main {
    public static void main(String[] args) {
        Tire tire = new Tire();
        tire.insert("one");
        tire.insert("two");
        tire.insert("one");
        System.out.println(tire.getSize());
        System.out.println(tire.contains("tw"));
        System.out.println(tire.isPrefix("tw"));
    }
}
