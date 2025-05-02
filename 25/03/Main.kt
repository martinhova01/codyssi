import java.io.File

class Solution(var test: Boolean) {
    val filename: String = if (test) "testinput.txt" else "input.txt"
    val data: String = File(filename).readText().trim()
    var ranges: MutableList<IntRange> = mutableListOf<IntRange>()
    var piles: MutableList<MutableSet<Int>> = mutableListOf()

    init {
        for (line in data.split("\n")) {
            var ranges: List<String> = line.split(" ")
            for (range in ranges) {
                var start_stop = range.split("-")
                this.ranges.add(start_stop[0].trim().toInt()..start_stop[1].trim().toInt())
            }
        }
    }

    fun part1(): Int {
        var s = 0
        for (r in this.ranges) {
            s += r.last - r.first + 1
        }
        return s
    }

    fun part2(): Int {
        var s = 0
        for (i in 0..this.ranges.size - 2 step 2) {
            var pile: MutableSet<Int> = mutableSetOf()
            for (j in this.ranges[i]) {
                pile.add(j)
            }
            for (j in this.ranges[i + 1]) {
                pile.add(j)
            }
            this.piles.add(pile)
            s += pile.size
        }
        return s
    }

    fun part3(): Int {
        var max = 0
        for (i in 0..this.piles.size - 2) {
            max = maxOf(max, this.piles[i].union(this.piles[i + 1]).size)
        }
        return max
    }
}

fun main() {
    var s = Solution(true)
    println("---TEST---")
    println("part1: " + s.part1())
    println("part2: " + s.part2())
    println("part3: " + s.part3() + "\n")
    
    s = Solution(false)
    println("---Main---")
    println("part1: " + s.part1())
    println("part2: " + s.part2())
    println("part3: " + s.part3())
}