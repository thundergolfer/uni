package org.commonmark.testutil.example;

public class Example {

    private final String filename;
    private final String section;
    private final String info;
    private final int exampleNumber;
    private final String source;
    private final String html;

    public Example(String filename, String section, String info, int exampleNumber, String source, String html) {
        this.filename = filename;
        this.section = section;
        this.info = info;
        this.exampleNumber = exampleNumber;
        this.source = source;
        this.html = html;
    }

    public String getInfo() {
        return info;
    }

    public String getSource() {
        return source;
    }

    public String getHtml() {
        return html;
    }

    @Override
    public String toString() {
        return "File \"" + filename + "\" section \"" + section + "\" example " + exampleNumber;
    }
}
