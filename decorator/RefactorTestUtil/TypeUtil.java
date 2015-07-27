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
