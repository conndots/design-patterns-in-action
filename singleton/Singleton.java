public class Singleton {
    /**
    * Not a good way to implement Singleton
    */
    public static Class SingletonWithDoubleCheckedLockingUnsafeEdition {
        private static SingletonWithDoubleCheckedLockingUnsafeEdition INSTANCE = null;
        private static final Object LOCK = new Object();

        public static SingletonWithDoubleCheckedLockingUnsafeEdition getInstance() {
            if (INSTANCE == null) {
                synchronized(LOCK) {
                    if (INSTANCE == null) {
                        INSTANCE = new SingletonWithDoubleCheckedLockingUnsafeEdition();
                    }
                }
            }
            return INSTANCE;
        }

        private SingletonWithDoubleCheckedLockingUnsafeEdition() {}
    }

    public static class SingletonWithDoubleCheckedLockingFineEdition {
        private static volatile SingletonWithDoubleCheckedLockingFineEdition INSTANCE = null;
        private static final Object LOCK = new Object();

        public static SingletonWithDoubleCheckedLockingFineEdition getInstance() {
            if (INSTANCE == null) {
                synchronized(LOCK) {
                    if (INSTANCE == null) {
                        INSTANCE = new SingletonWithDoubleCheckedLockingFineEdition();
                    }
                }
            }
            return INSTANCE;
        }

        private SingletonWithDoubleCheckedLockingFineEdition() {}
    }

    public static Class SingletonWithStaticFinalField {
        private static final SingletonWithStaticFinalField INSTANCE = new SingletonWithStaticFinalField();
        public static SingletonWithStaticFinalField getInstance() {
            return INSTANCE;
        }
    }

    public static class SingletonWithNestedClass {
        private static class SingletonHolder {
            private static final SingletonWithNestedClass INSTANCE = new SingletonWithNestedClass();
        }
        private SingletonWithNestedClass() {}
        public static final SingletonWithNestedClass getInstance() {
            return SingletonHolder.INSTANCE;
        }
    }

    public static enum SingletonWithEnum {
        INSTANCE;
    }
}
