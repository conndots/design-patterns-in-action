import org.slf4j.Logger;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.AbstractMap;
import java.util.Map;

public class RefactorTestUtil {
    private static Logger LOGGER = null;

    public interface Equality <T, S> {
        public boolean isEqual(T obj0, S obj1);
    }

    public static void setLogger(Logger logger) {
        LOGGER = logger;
    }

    @Target( ElementType.METHOD )
    @Retention( RetentionPolicy.RUNTIME )
    public @interface RefactorTest {
        String classRef();
        String methodName();
        int[] paramClassIndex2ThisParams() default {};
    }

    private static void testFailLog(String message, Map.Entry<Class<?>, String> migTo, Map.Entry<Class<?>, String>
            migFrom, Object ... params) {
        String argsStr = null;
        if (params != null && params.length > 0) {
            StringBuilder args = new StringBuilder();
            for (Object param : params) {
                args.append(param).append(":").append(param.getClass().getSimpleName());
                args.append(",");
            }
            if (args.length() > 0) {
                argsStr = args.substring(0, args.length() - 1);
            }
            else {
                argsStr = args.toString();
            }
        }
        String logStr = String.format("[MigrationTest]%s-TO(%s)-FROM-(%s)-ARGS(%s)", message, migTo.toString(),
                migFrom.toString(), argsStr);

        if (LOGGER != null) {
            LOGGER.error(logStr);
        }
        else {
            System.err.println(logStr);
        }
    }

    public static <T> T decorateFunctionWithRefactorTest(Class<?> cls, String method, Object ... params) throws
            NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        return decorateFunctionWithRefactorTest(cls, method, new Equality<T, Object>() {
            public boolean isEqual(T obj0, Object obj1) {
                return obj0.equals(obj1);
            }
        }, params);
    }

    public static <T, S> T decorateFunctionWithRefactorTest(Class<?> cls, String method, Equality<T, S> equals, Object
            ... params) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        Method refactorTo = TypeUtil.getClassMethodWithNotAccurateTypedParams(cls, method, params);
        if (refactorTo == null) {
            throw new NoSuchMethodException(String.format("There is no method %s in class %s", method, cls
                    .getSimpleName()));
        }

        T toResult = (T) refactorTo.invoke(null, params);

        RefactorTest refactorAnno = refactorTo.getAnnotation(RefactorTest.class);
        String refactorFromCls =  refactorAnno.classRef();
        String refactorFromMethod = refactorAnno.methodName();
        int[] paramClassesIndex = refactorAnno.paramClassIndex2ThisParams();

        try {
            Class<?> refactorFromClass = ClassLoader.getSystemClassLoader().loadClass(refactorFromCls);


            Object[] fromParams = null;
            if (paramClassesIndex != null && paramClassesIndex.length > 0) {
                fromParams = new Object[paramClassesIndex.length];
                for (int i = 0; i < paramClassesIndex.length; i ++) {
                    fromParams[i] = params[paramClassesIndex[i]];
                }
            }
            else {
                fromParams = params;
            }

            Method refactorFrom = TypeUtil.getClassMethodWithNotAccurateTypedParams(refactorFromClass, refactorFromMethod,
                    fromParams);
            if (refactorFrom == null) {
                testFailLog("No refactor-from method found", new AbstractMap.SimpleEntry<Class<?>, String>(cls, method)
                        , new AbstractMap.SimpleEntry<Class<?>, String>(refactorFromClass, refactorFromMethod), params);
                return toResult;
            }

            S fromResult = (S) refactorFrom.invoke(null, fromParams);

            if (! equals.isEqual(toResult, fromResult)) {
                testFailLog("Not equal after refactoring", new AbstractMap.SimpleEntry<Class<?>, String>(cls, method)
                        , new AbstractMap.SimpleEntry<Class<?>, String>(refactorFromClass, refactorFromMethod), params);
            }


        } catch (ClassNotFoundException e) {
            testFailLog("No refactor-from Class found", new AbstractMap.SimpleEntry<Class<?>, String>(cls, method)
                    , new AbstractMap.SimpleEntry<Class<?>, String>(null, refactorFromMethod), params);

        } finally {
            return toResult;
        }
    }
}
