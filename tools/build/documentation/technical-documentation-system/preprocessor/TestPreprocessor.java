package preprocessor;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class TestPreprocessor {
    @Test(expected = ReferenceProcessingException.class)
    public void testToParseInvalidDirectiveWithTooManyParts() throws Exception {
        String testDirective = "%% foo bar bee 4-4 %%";
        Preprocessor.Substitution sub = Preprocessor.parseSubstitution(testDirective);
    }
}
