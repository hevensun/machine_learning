import java.math.BigDecimal;

public class Utils {
    public static Boolean isNumber(String text){
        try {
            String str = new BigDecimal(text).toString();
        }catch (Exception e){
            return false;
        }
        return true;
    }
}
