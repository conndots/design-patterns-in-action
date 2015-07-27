import com.google.common.collect.Lists;
import com.google.common.collect.Sets;
import org.apache.commons.collections.CollectionUtils;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.lang3.StringUtils;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class CollectionsUtil {
    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "empty"
    )
    public static <K, V> boolean empty(Map<K, V> map) {
        return MapUtils.isEmpty(map);
    }

    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "empty"
    )
    public static <T> boolean empty(List<T> list) {
        return CollectionUtils.isEmpty(list);
    }

    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "empty"
    )
    public static <T> boolean empty(Set<T> set) {
        return CollectionUtils.isEmpty(set);
    }

    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "empty"
    )
    public static boolean empty(String str) {
        return StringUtils.isEmpty(str);
    }

    /**
     * check whether a Map or a Set or List or a String is empty. Lack the type parameters for downward compatibility
     * of Tatooine submodules.
     * @param col
     * @return
     */
    @Deprecated
    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "empty"
    )
    public static boolean empty(Object col) {
        if (col == null) {
            return true;
        }
        Class cls = col.getClass();
        if (col instanceof Map) {
            Map map = (Map) col;
            return map.size() < 1;
        }
        if (col instanceof Set) {
            Set set = (Set) col;
            return set.size() < 1;
        }
        if (col instanceof List) {
            List list = (List) col;
            return list.size() < 1;
        }
        String tmp = col.toString();
        if (tmp.equals("") || tmp.equals("0") || tmp.equals("false")) {
            return true;
        }
        return false;
    }

    /**
     * No type argument. Not recommended to use.
     * @param arr
     * @return
     */
    @Deprecated
    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "notEmpty"
    )
    public static boolean notEmpty(Object arr) {
        return !empty(arr);
    }


    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "notEmpty"
    )
    public static <T> boolean notEmpty(List<T> list) {
        return CollectionUtils.isNotEmpty(list);
    }


    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "notEmpty"
    )
    public static <T> boolean notEmpty(Set<T> set) {
        return CollectionUtils.isNotEmpty(set);
    }


    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "notEmpty"
    )
    public static <K, V> boolean notEmpty(Map<K, V> map) {
       return MapUtils.isNotEmpty(map);
    }


    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "notEmpty"
    )
    public static boolean notEmpty(String str) {
        return StringUtils.isNotEmpty(str);
    }

    /**
     * Whether the given collection contains the obj. The collection could be a List, Set, Map, Array. When it is a
     * Map, it checks whether the values of the Map contains obj. Deprecated.
     * @param collection
     * @param obj
     * @return
     */
    @Deprecated
    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "inArray"
    )
    public static boolean inCollection(Object collection, Object obj) {
        if ((collection == null) || (obj == null)) {
            return false;
        }
        Class cls = collection.getClass();
        if (collection instanceof List) {
            List list = (List) collection;
            return list.contains(obj);
        }
        if (collection instanceof Set) {
            Set set = (Set) collection;
            return set.contains(obj);
        }
        if (collection instanceof Map) {
            Map map = (Map) collection;
            return map.values().contains(obj);
        }

        Object[] objs = (Object[]) collection;
        for (Object elem : objs) {
            if (elem.equals(obj)) {
                return true;
            }
        }
        return false;
    }


    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "inArray"
    )
    public static <T> boolean inCollection(Collection<T> collection, T elem) {
        return null != collection && collection.contains(elem);
    }

    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "inArray"
    )
    public static <K, V> boolean inCollection(Map<K, V> map, V value) {
        return null != map && map.containsValue(value);
    }

    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "inArray"
    )
    public static <T> boolean inCollection(T[] array, T elem) {
        if (array == null || array.length == 0) {
            return false;
        }
        for (T obj : array) {
            if (obj.equals(elem)) {
                return true;
            }
        }
        return false;
    }

    @RefactorTestUtil.RefactorTest(
            classRef = "com.meituan.rc.risk.util.PhpUtils",
            methodName = "arrayUnique"
    )
    public static <T> List<T> getDuplicatesRemovedList(List<T> list) {
        if (list == null) {
            return null;
        }
        if (CollectionUtils.isEmpty(list)) {
            return Lists.newArrayList();
        }

        Set<T> set = Sets.newHashSet(list);
        return Lists.newArrayList(set);
    }

}
