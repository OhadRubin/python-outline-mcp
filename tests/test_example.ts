// Simple TypeScript test file
interface User {
    name: string;
    age: number;
}

function greet(user: User): string {
    return `Hello, ${user.name}!`;
}

export function calculateSum(a: number, b: number): number {
    return a + b;
}

class Calculator {
    private history: string[] = [];
    
    constructor() {}
    
    public add(a: number, b: number): number {
        const result = a + b;
        this.history.push(`${a} + ${b} = ${result}`);
        return result;
    }
    
    static multiply(x: number, y: number): number {
        return x * y;
    }
    
    protected getHistory(): string[] {
        return this.history;
    }
}

export class MathUtils extends Calculator {
    async power(base: number, exponent: number): Promise<number> {
        return Math.pow(base, exponent);
    }
}