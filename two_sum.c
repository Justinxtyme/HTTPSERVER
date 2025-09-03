//the digital root of a positive integer
// can be reduced to (num - 1) % 9 + 1
// so for summing all digits until the 
// sum is < 10, this is all we need

int addDigits(int num) {
    if (num == 0) {
        return 0;
    }
    return (num - 1) % 9 + 1;
}

//longer Loop Method

int addDigits(int num) {
    // Outer loop: continues until the number is a single digit
    while (num >= 10) {
        int sum = 0;
        
        // Inner loop: sums the digits of the current number
        while (num > 0) {
            sum += num % 10; // Get the last digit and add it to the sum
            num /= 10;      // Remove the last digit
        }
        
        num = sum; // The sum becomes the new number for the next iteration
    }
    
// and a recursion method //

// Helper function to sum the digits of a number
int sumDigits(int n) {
    if (n == 0) {
        return 0;
    }
    return (n % 10) + sumDigits(n / 10);
}

int addDigits(int num) {
    if (num < 10) {
        return num; // Base case: num is already a single digit
    }
    
    // Recursive step: sum the digits, then find the digital root of that sum
    return addDigits(sumDigits(num));
}