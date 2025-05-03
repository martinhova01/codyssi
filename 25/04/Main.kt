import java.io.File

class Solution(var test: Boolean) {
    val filename: String = if (test) "testinput.txt" else "input.txt"
    val data: String = File(filename).readText().trim()
    val alphabet: String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    fun memory_units(line: String): Int {
        var s = 0
        for (c in line) {
            s += if (c.isDigit()) c.digitToInt() else alphabet.indexOf(c) + 1
        }
        return s
    }

    fun lossy_compress(line: String): String {
        var num: Int = line.length / 10
        var res: String = line.substring(0, num)
        res += (line.length - num*2).toString()
        res += line.substring(line.length-num, line.length)
        return res
    }

    fun lossless_compress(line: String): String {
        var res: String = ""
        var current: Char = line[0]
        var count: Int = 1
        var i = 1
        while (i < line.length) {
            if (line[i].equals(current)) {
                count++
            }
            else {
                res += count.toString() + current
                current = line[i]
                count = 1
            }
            i++
        }

        res += count.toString() + current
        return res
    }

    fun part1(): Int {
        return data
            .lineSequence()
            .sumOf{memory_units(it)}
    }

    fun part2(): Int {
        return data
            .lineSequence()
            .map{lossy_compress(it)}
            .sumOf{memory_units(it)}
    }

    fun part3(): Int {
        return data
            .lineSequence()
            .map{lossless_compress(it)}
            .sumOf{memory_units(it)}   
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