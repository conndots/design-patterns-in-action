使用Java中的annotations实现decorator设计模式
===========
Decorator是一个经典的结构式设计模式，有着非常广泛的应用。在经典的*Design Patterns:Elements of Reusable Object-Oriented Software*中，它的用意被描述为：动态地为一个对象添加额外的责任与功能。对于扩展功能，装饰器提供了比子类化更加灵活的替代方案。  
在许多编程语言中，比如Python，在语法上就提供了装饰器的支持，能够透明地使用装饰器。而Java则相比之下繁琐一些，通过Decorator接口的各类实现，针对被decorate的组件接口的实现来装饰。本文介绍一种基于annotation的decorator实现，虽然无法实现如python一般的透明使用装饰器，在某些情景下，也是一种灵活的实现方式。  

#通过decorator实现refactor_test
我们想要通过装饰器实现这样的一个测试工具：我们重新实现了一个函数A，原函数是B。在调用函数A时，能够自动运行函数B，对二者的结果作比较，如果不相等，将当前的环境信息输出到日志中，以便追查。同时，不应现对函数的正常使用。  
这里的函数，我们要求是**幂等的**，**无副作用的**。  
下列全部的代码在[这里](https://github.com/conndots/design-patterns-in-action/tree/master/decorator/RefactorTestUtil)。
  
#Python的decorator
使用python能够非常轻易地实现装饰器@refactor_test。代码如下([GitHub](https://github.com/conndots/design-patterns-in-action/blob/master/decorator/RefactorTestUtil/refactor_test.py))：  
  
```
import functools
import logging

LOGGER = logging.getLogger('refactor_test')

def refactor_test(comp_func):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kws):
            comp_res = comp_func(*args, **kws)
            res = func(*args, **kws)
            if res != comp_res:
                message = "not equals for function:{} from {} 
                        with arguments:{}-{}".format(func.__name__, 
                                comp_func.__name__, args, kws)
                LOGGER.debug(message)
                print(message)
            return res
        return wrapper
    return decorator

def refactor_from(message):
    return message

@refactor_test(refactor_from)
def refactor_to0(message):
    return message

@refactor_test(refactor_from)
def refactor_to1(message):
    return "!" + message

if __name__ == '__main__':
    refactor_to0('Hello python!')
    refactor_to1('Hello python!')
```
  
这是非常经典的python decorator实现，是完全透明的，调用者无需关注到我们在调用时候执行了一个refacor_test的过程。refactor_to0是一个符合要求的重构实现，而refactor_to1不是。    

#Java实现
由于java语法的限制，无法像动态语言python一样透明地为给定方法添加decorator。当然可以按照经典的设计实现，如下图所示。
![](https://upload.wikimedia.org/wikipedia/commons/e/e9/Decorator_UML_class_diagram.svg)
  
对于我们想要解决的问题，在python中，通过装饰器语法，在编码时，就指定了由重构后方法到重构前方法的映射。而如果按照传统的方法实现，我们首先，需要维护一个重构后的方法到重构之前方法的映射表，另外，我们不能为每一个重构的方法都编写一个装饰器方法，不够灵活，过于繁琐。所以，我们需要使用java的反射机制，动态调用方法。第一点也是很繁琐的，或者写到配置文件，或者hard code到代码里，都是极不好的。我们通过java的annotation注解功能来实现。Oracle的[官方tutorial](https://docs.oracle.com/javase/tutorial/java/annotations/)中，有对java annotations比较细致的说明。我们来看看如何实现。
  
RefactorUtil.java ([GitHub](https://github.com/conndots/design-patterns-in-action/blob/master/decorator/RefactorTestUtil/RefactorTestUtil.java)):  
  
```
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

    public static <T, S> T decorateFunctionWithRefactorTest(Class<?> cls, String method, 
            Equality<T, S> equals, Object... params) throws NoSuchMethodException,   
            InvocationTargetException, IllegalAccessException {
        Method refactorTo = TypeUtil.getClassMethodWithNotAccurateTypedParams(cls, method,
                 params);
        if (refactorTo == null) {
            throw new NoSuchMethodException(String.format("There is no method %s in class 
                    %s", method, cls
                    .getSimpleName()));
        }

        T toResult = (T) refactorTo.invoke(null, params);

        RefactorTest refactorAnno = refactorTo.getAnnotation(RefactorTest.class);
        String refactorFromCls =  refactorAnno.classRef();
        String refactorFromMethod = refactorAnno.methodName();
        int[] paramClassesIndex = refactorAnno.paramClassIndex2ThisParams();

        try {
            Class<?> refactorFromClass = ClassLoader.getSystemClassLoader()
                    .loadClass(refactorFromCls);


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

            Method refactorFrom = TypeUtil.getClassMethodWithNotAccurateTypedParams
                    (refactorFromClass, refactorFromMethod,
                    fromParams);
            if (refactorFrom == null) {
                testFailLog("No refactor-from method found", new AbstractMap.
                        SimpleEntry<Class<?>, String>(cls, method)
                        , new AbstractMap.SimpleEntry<Class<?>,String>
                        (refactorFromClass, refactorFromMethod), params);
                return toResult;
            }

            S fromResult = (S) refactorFrom.invoke(null, fromParams);

            if (! equals.isEqual(toResult, fromResult)) {
                testFailLog("Not equal after refactoring", new AbstractMap.SimpleEntry
                        <Class<?>, String>(cls, method)
                        , new AbstractMap.SimpleEntry<Class<?>, String>
                        (refactorFromClass, refactorFromMethod), params);
            }


        } catch (ClassNotFoundException e) {
            testFailLog("No refactor-from Class found", new AbstractMap.SimpleEntry
                    <Class<?>, String>(cls, method), new AbstractMap.SimpleEntry<Class<?>,  
                    String>(null, refactorFromMethod), params);

        } finally {
            return toResult;
        }
    }
}
```

RefactorTestUtil.decorateFunctionWithRefactorTest()方法通过传入对应类与方法名，还有参数列表，通过RefactorTest注解获取该方法对应重构前方法，动态比较两次调用的结果是否一致，决定是否计入日志。  
@interface RefactorTest是一个注解的声明，再待注解的方法前添加@RefactorTest(...)，通过三个属性classRef，methodName，paramClassIndex2ThisParams来给定重构前方法及调用参数的不对齐问题。  
通过注解和反射我们实现了这个功能，而由于java反射的限制，对于参数列表的类型不是方法签名中参数列表的类型完全匹配无法找到确定的方法，我实现了TypeUtil，提供了简单的动态机制，找到对应方法。比如size(Collection)方法，再传入一个Set时，仅仅通过java的反射API，无法找到size(Collection)方法。  
  
TypeUtil.java([GitHub](https://github.com/conndots/design-patterns-in-action/blob/master/decorator/RefactorTestUtil/TypeUtil.java)):  
  
```
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class TypeUtil {
    public static boolean isMatchedBoxingType(Class<?> cls0, Class<?> cls1) {
        if (cls0 == null || cls1 == null) {
            return false;
        }
        if (! cls0.isPrimitive() && ! cls1.isPrimitive()) {
            return cls0.equals(cls1);
        }
        if (cls0.isPrimitive() && cls1.isPrimitive()) {
            return cls0.equals(cls1);
        }

        Class<?> primitive = cls0.isPrimitive() ? cls0 : cls1, boxing = cls1.isPrimitive() ? cls0 : cls1;

        if (primitive.equals(int.class)) {
            return boxing.equals(Integer.class);
        }
        if (primitive.equals(short.class)) {
            return boxing.equals(Short.class);
        }
        if (primitive.equals(float.class)) {
            return boxing.equals(Float.class);
        }
        if (primitive.equals(double.class)) {
            return boxing.equals(Double.class);
        }
        if (primitive.equals(boolean.class)) {
            return boxing.equals(Boolean.class);
        }
        if (primitive.equals(long.class)) {
            return boxing.equals(Long.class);
        }
        if (primitive.equals(char.class)) {
            return boxing.equals(Character.class);
        }
        if (primitive.equals(byte.class)) {
            return boxing.equals(Byte.class);
        }
        return false;
    }

    private static boolean isSubClassOf(Class<?> subCls, Class<?> superCls) {
        if (subCls == null || superCls == null) {
            return false;
        }
        if (superCls.equals(Object.class)) {
            return true;
        }
        if (superCls.isInterface() && ! subCls.isInterface()) {
            for (Class<?> interf : subCls.getInterfaces()) {
                if (interf.equals(superCls)) {
                    return true;
                }
            }
            return false;
        }
        Class<?> cls = subCls;
        for (; cls != null && ! cls.equals(superCls); cls = cls.getSuperclass());
        return cls != null;
    }

    public static Method getClassMethodWithNotAccurateTypedParams(Class<?> cls, String methodName, Object ...
            params) {
        if (cls == null || methodName == null) {
            return null;
        }

        Class<?>[] paramClasses = new Class<?>[params.length];
        int i = 0;
        for (Object param : params) {
            paramClasses[i++] = param.getClass();
        }

        Method method = null;
        try {
            method = cls.getMethod(methodName, paramClasses);
        } catch (NoSuchMethodException e) {
            Method[] methods = cls.getMethods();

            List<Method> capableMethods = new ArrayList<Method>();
            for (Method candidateMethod : methods) {
                if (! candidateMethod.getName().equals(methodName)) {
                    continue;
                }
                if (! candidateMethod.isVarArgs() && candidateMethod.getParameterTypes().length != params.length) {
                    continue;
                }

                Class<?>[] methodParamClasses = candidateMethod.getParameterTypes();
                boolean found = true;
                for (int j = 0; j < methodParamClasses.length; j ++) {
                    Class<?> methodParamClass = methodParamClasses[j];
                    if(! TypeUtil.isInstanceOf(methodParamClass, params[j])) {
                        found = false;
                        break;
                    }
                }

                if (found) {
                    capableMethods.add(candidateMethod);
                }
            }

            if (capableMethods.size() == 1) {
                method = capableMethods.get(0);
            }
            else if (capableMethods.size() > 1) {
                for (int pi = 0; pi < params.length; pi ++) {
                    Class<?> bottom = Object.class;
                    int mindex = 0;
                    int bottomCount = 0;
                    for (int mi = 0; mi < capableMethods.size(); mi ++) {
                        Method m = capableMethods.get(mi);
                        Class<?> pclass = m.getParameterTypes()[pi];
                        if (pclass.equals(bottom) || isMatchedBoxingType(pclass, bottom)) {
                            bottomCount ++;
                            continue;
                        }
                        if (isSubClassOf(pclass, bottom)) {
                            bottom = pclass;
                            mindex = mi;
                            bottomCount = 1;
                        }
                    }
                    if (bottomCount < capableMethods.size() && bottomCount > 0) {
                        method = capableMethods.get(mindex);
                        break;
                    }
                }
            }
        }
        return method;
    }

    public static boolean isInstanceOf(Class<?> cls, Object instance) {
        if (cls == null) {
            return false;
        }

        if (instance == null) {
            return true;
        }

        if (cls.isPrimitive()) {
            Class<?> insType = instance.getClass();
            return isMatchedBoxingType(cls, insType);
        }
        else if (cls.isArray()) {
            Class<?> insType = instance.getClass();
            if (! insType.isArray()) {
                return false;
            }
            Class<?> cls0 = cls.getComponentType(), cls1 = insType.getComponentType();
            if (isMatchedBoxingType(cls0, cls1)) {
                return true;
            }
        }
        return cls.isInstance(instance);
    }
}
```  
  
比如我们有4个方法：  
  
```
public class Util {
    public static String refactorFrom(String message, int time) {
        return message + "(" + time + ")";
    }
    
    @RefactorTestUtil.RefactorTest(
        classRef = "Util",
        methodName = "refactorFrom"
    )
    public static String refactorTo0(String message, int time) {
        return message + "(" + time + ")";
    }
    
    @RefactorTestUtil.RefactorTest(
        classRef = "Util",
        methodName = "refactorFrom",
        paramClassIndex2ThisParams = {1, 0}
    )
    public static String refactorTo1(int time, String message) {
        return message + "(" + time + ")";
    }
    
    @RefactorTestUtil.RefactorTest(
        classRef = "Util",
        methodName = "refactorFrom"
    )
    public static String refactorTo2(String message, int time) {
        return message + "[" + time + "]";
    }
```    

refactorTo0, refactorTo1, refactorTo2都是重构自refactorFrom。其中refactorTo1更换了参数类型的顺序，使用了paramClassIndex2ThisParams参数。而refactorTo2是一个会被报告错误的重构函数。我们做如下的测试：  
  
```
public RefactorTestUtilTest {
    @Test
    public void testDecorateFunctionWithRefactorTest() {
        String message = "OK";
        int time = 3;
        
        assertEquals(message + "(" + time + ")", RefactorUtil.
                decorateFunctionWithRefactorTest(Util.class, "refactorTo0", message, time);
        assertEquals(message + "(" + time + ")", RefactorUtil.
                decorateFunctionWithRefactorTest(Util.class, "refactorTo1", time, message);
        assertEquals(message + "[" + time + "]", RefactorUtil.
                decorateFunctionWithRefactorTest(Util.class, "refactorTo2", message, time);
    }
}
```
  
这样，通过java的annotations，我们实现了一种特定需求的decorator设计模式，但是由于语言特性与语法，无法实现python一样的透明使用。  
