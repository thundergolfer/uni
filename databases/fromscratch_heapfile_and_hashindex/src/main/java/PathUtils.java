public class PathUtils {
    public static String constructHeapfilePath(int pageSize) {
        StringBuilder builder = new StringBuilder();
        builder.append("heap");
        builder.append(".");
        builder.append(String.valueOf(pageSize));

        return builder.toString();
    }
}
