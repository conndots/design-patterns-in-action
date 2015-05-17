/*
Adapter to implement duckType by java
*/

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;


interface Addable<T> {
    void add(T t);
}

class Fill {
    //Classtoken version
    public static <T> void fill(Addable<T> addable, Class<? extends T> classToken, 
            int size){
        for(int i = 0; i < size; i ++){
            try {
                addable.add(classToken.newInstance());
            } catch (InstantiationException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (IllegalAccessException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }   

//  //generator version
//  public static <T> void fill(Addable<T> addable, Generator<T> generator, 
//          int size) {
//      for(int i = 0; i < size; i ++) {
//          addable.add(generator.next());
//      }
//  }
}

class AddableCollectionAdapter<T> implements Addable<T> {
    private Collection<T> c;
    public AddableCollectionAdapter(Collection<T> c) {
        this.c = c;
    }
    @Override
    public void add(T t) {
        c.add(t);
    }
}

class Adapter {
    public static <T> Addable<T> collectionAdapter(Collection<T> c){
        return new AddableCollectionAdapter<T>(c);
    }
}

class Coffee {}
class Latte extends Coffee {}
class Mocha extends Coffee {}

public class Adapter2Duck {
    public static void main(String[] args){
        List<Coffee> carrier = new ArrayList<Coffee>();
        Fill.fill(Adapter.collectionAdapter(carrier), Coffee.class, 3);
        Fill.fill(Adapter.collectionAdapter(carrier), Latte.class, 2);
        Fill.fill(Adapter.collectionAdapter(carrier), Mocha.class, 1);
    }
}