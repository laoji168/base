package main

import (
    "bufio"
    "fmt"
    "mlib"
    "mp"
    "os"
    "strconv"
    "strings"
)

var lib *library.MusicManager
var id int = 1
var ctrl, signal chan int

func handleLibCommands(tokens []string)  {
    switch tokens[1] {
    case "list":
        for i:=0; i<lib.Len(); i++ {
            e, _ := lib.Get(i)
            fmt.Println(i + 1, ":", e.Name, e.Artist, e.Source, e.Type)
        }
    case "add":
        if len(tokens) == 7 {
            id++
            lib.Add(&library.MusicEntry{strconv.Itoa(id), tokens[2], tokens[3], tokens[4], tokens[5], tokens[6]})
        } else {
            fmt.Println("USAGE : lib add <name><artist><genre><source><type> (7 argv)")
        }
    case "remove":
        if len(tokens) == 3 {
            lib.RemoveByName(tokens[2])
        } else {
            fmt.Println("USAGE: lib remove <name>")
        }
    default:
        fmt.Println("Unrecogized lib command: ", tokens[1])
    }
}

func handlePlayCommands(tokens []string)  {
    if len(tokens) != 2 {
        fmt.Println("USAGE:play<name>")
        return
    }
    e := lib.Find(tokens[1])
    if e == nil {
        fmt.Println("The music", tokens[1], "does not exist.")
        return
    }
    mp.Play(e.Source, e.Type)
}

func main() {
    fmt.Println(`
     Enter following commands to control the player:
     lib list --View the existing music lib
     lib add <name><artist><genre><source><type> -- Add a music to the music lib
     lib remove <name> --Remove the specified music from the lib
     play <name> -- Play the specified music
     `)
    lib = library.NewMusicManager()
    r := bufio.NewReader(os.Stdin)

    for i:=0; i<100; i++ {
        fmt.Print("Enter command-> ")
        rawline, _, _ := r.ReadLine()
        line := string(rawline)
        if line == "q" || line == "e" {
            break
        }
        tokens := strings.Split(line, " ")
        if tokens[0] == "lib" {
            handleLibCommands(tokens)
        } else if tokens[0] == "play" {
            handlePlayCommands(tokens)
        } else {
            fmt.Println("Unrecognized command :", tokens[0])
        }
    }
}