require "singleton"

class A
    include Singleton

    def initialize
        puts "initialize object of A"
    end
end

class B
    include Singleton

    def initialize
        puts "initialize object of B"
    end
end

prev_a = nil
prev_b = nil
for i in 0 .. 5
    a = A.instance
    b = B.instance
    if prev_a == nil && prev_b == nil
        prev_a, prev_b = a, b
    else
        puts "a equals? #{prev_a == a} b equals? #{prev_b == b}"
    end
end