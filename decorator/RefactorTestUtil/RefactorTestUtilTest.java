import org.junit.Test;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.Assert.*;

public class RefactorTestUtilTest {
    @Test
    public void testDecorateFunctionWithRefactorTest() throws Exception {
        assertTrue(((List) RefactorTestUtil.decorateFunctionWithRefactorTest(CollectionsUtil.class,
                "getDuplicatesRemovedList", new RefactorTestUtil.Equality<List, Object>() {
                    public boolean isEqual(List obj0, Object obj1) {
                        Set set0 = new HashSet(obj0), set1 = new HashSet((List) obj1);
                        return set0.equals(set1);
                    }
                },Arrays.asList("a", "v", "B", "a", "v"))).size() == 3);
        assertTrue((Boolean) RefactorTestUtil.decorateFunctionWithRefactorTest(CollectionsUtil.class, "empty", new
                HashMap<String, Integer>()));
    }

}