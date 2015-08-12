require "observer"

#object
class Tick
    include Observable

    def tick
        loop do
            now = Time.now
            changed
            notify_observers(now.hour, now.min, now.sec)
            sleep 1.0 - Time.now.usec / 1000000.0
        end
    end
end

#observer
class TextClock
    def initialize(target, name)
        @name = name
        target.add_observer(self)
    end

    def update(hour, min, sec)
        puts "#{@name} [#{hour}:#{min}:#{sec}]"
        STDOUT.flush
    end
end

tick = Tick.new
clock0 = TextClock.new(tick, "Clock A")
clock1 = TextClock.new(tick, "Clock B")
tick.tick