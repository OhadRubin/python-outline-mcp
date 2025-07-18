// Simple JavaScript test file
function greet(name) {
    return `Hello, ${name}!`;
}

export function calculateSum(a, b) {
    return a + b;
}

class Calculator {
    constructor() {
        this.history = [];
    }
    
    add(a, b) {
        const result = a + b;
        this.history.push(`${a} + ${b} = ${result}`);
        return result;
    }
    
    static multiply(x, y) {
        return x * y;
    }
}

export class MathUtils extends Calculator {
    async power(base, exponent) {
        return Math.pow(base, exponent);
    }
}