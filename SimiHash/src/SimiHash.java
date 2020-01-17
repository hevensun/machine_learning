import java.math.BigInteger;
import java.util.*;

/**
 * Created by slade on 2019/12/27.
 */
public class SimiHash {
    private String token;
    private BigInteger intSimHash;
    private String strSimHash;
    private int hashsize = 64;

    public SimiHash() {
    }

    public SimiHash(String token) {
        this.token = token;
        this.intSimHash = simHash();
    }

    public SimiHash(String token, int hashsize) {
        this.token = token;
        this.hashsize = hashsize;
        this.intSimHash = simHash();
    }

    HashMap<String, Integer> wordMap = new HashMap<>();

    public BigInteger simHash() {
//        初始化
//        用来统计不同位置上的1和0的个数
        int[] v = new int[this.hashsize];
        StringTokenizer stringTokenizer = new StringTokenizer(this.token);
        while (stringTokenizer.hasMoreTokens()) {
            String temp = stringTokenizer.nextToken();
//            hash
            BigInteger t = this.hash(temp);
            for (int i = 0; i < this.hashsize; i++) {
                BigInteger bitmask = new BigInteger("1").shiftLeft(i);
                if (t.and(bitmask).signum() != 0) {
//                    v即为整句话上hash后的w的add汇总向量值
                    v[i]++;
                } else {
                    v[i]--;
                }
            }
        }

        BigInteger fingerprint = new BigInteger("0");
        StringBuffer simHashBuffer = new StringBuffer();
        for (int i = 0; i < this.hashsize; i++) {
            if (v[i] >= 0) {
//                还原为10进制
                fingerprint = fingerprint.add(new BigInteger("1").shiftLeft(i));
//                正负样本的二进制表示
                simHashBuffer.append("1");
            } else {
                simHashBuffer.append("0");
            }
        }
        this.strSimHash = simHashBuffer.toString();
        return fingerprint;
    }

    public BigInteger hash(String s) {
        if (s == null || s.length() == 0) {
            return new BigInteger("0");
        }
        char[] schar = s.toCharArray();
        BigInteger x = BigInteger.valueOf(((long) schar[0]) << 7);
        BigInteger m = new BigInteger("1000003");
        BigInteger mask = new BigInteger("2").pow(this.hashsize).subtract(new BigInteger("1"));
        for (char item : schar) {
            BigInteger temp = BigInteger.valueOf((long) item);
            x = x.multiply(m).xor(temp).and(mask);
        }
        x = x.xor(new BigInteger(String.valueOf((long) s.length())));

        if (x.equals(new BigInteger("-1"))) {
            x = new BigInteger("-2");
        }
        return x;
    }


    public int hanmingDist(SimiHash o) {
        BigInteger x = this.intSimHash.xor(o.intSimHash);
        int total = 0;
        while (x.signum() != 0) {
            total += 1;
//            统计x中二进制位数为1的个数
//            n&(n-1)每进行一次，则计数+1，最后一个位置上的1及以后的位置均被置为0
            x = x.and(x.subtract(new BigInteger("1")));
        }
        return total;
    }

    public int getDistince(String str1, String str2) {
        int distince = 0;
        if (str1.length() != str2.length()) {
            distince = -1;
        } else {
            for (int i = 0; i < str1.length(); i++) {
                if (str1.charAt(i) != str2.charAt(i)) {
                    distince++;
                }
            }
        }
        return distince;
    }


    public List subByDistance(SimiHash simiHash, int partition) {
        int groupNum = this.hashsize / partition;
        List v = new ArrayList<>();
        StringBuffer s = new StringBuffer();
        for (int i = 0; i < this.intSimHash.bitLength(); i++) {
            boolean sr = simiHash.intSimHash.testBit(i);

            if (sr) {
                s.append("1");
            } else {
                s.append("0");
            }

            if ((i + 1) % groupNum == 0) {
                // 将二进制转为BigInteger
                BigInteger eachValue = new BigInteger(s.toString(), 2);
                s.delete(0, s.length());
                v.add(eachValue);
            }
        }
        return v;
    }

}
