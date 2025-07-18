// Simple Java test file
public class Calculator {
    private java.util.List<String> history;
    
    public Calculator() {
        this.history = new java.util.ArrayList<>();
    }
    
    public int add(int a, int b) {
        int result = a + b;
        history.add(a + " + " + b + " = " + result);
        return result;
    }
    
    public static int multiply(int x, int y) {
        return x * y;
    }
    
    protected java.util.List<String> getHistory() {
        return history;
    }
}

interface MathOperations {
    int calculate(int a, int b);
}

enum Operation {
    ADD, SUBTRACT, MULTIPLY, DIVIDE
}