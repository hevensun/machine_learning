/**
 * Created by slade on 2019/12/27.
 */
public class Main {
    public static void main(String[] args) {
        SimiHash simiHash = new SimiHash("我 爱 中国 我 爱 中国 中国 中国");
        SimiHash simiHash1 = new SimiHash("魏 爱 中国 我 爱 中国 中国 中国");
        SimiHash simiHash2 = new SimiHash("我是蓝翔技工拖拉机学院手扶拖拉机专业的。不用多久，我就会升职加薪，当上总经理，出任CEO，走上人生巅峰。");
        System.out.println(simiHash.hanmingDist(simiHash1));
        System.out.println(simiHash.hanmingDist(simiHash));

        System.out.println(simiHash2.simHash());
    }
}
