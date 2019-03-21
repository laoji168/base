package main

import (
    "fmt"
)

type PersonInfo struct {
    Id string
    Name string
    Address string
}

func main() {
    var personDB map[string]PersonInfo
    personDB = make(map[string]PersonInfo)

    personDB["12345"] = PersonInfo{"12345", "Tom", "room203, ..."}
    personDB["1"] = PersonInfo{"1", "jack", "room101, ..."}

    person, ok := personDB["1234"]
    if ok {
        fmt.Println("Found Person", person.Name, "with ID 1234")
    } else {
        fmt.Println("Did not found person with ID 1234")
    }

    person, ok = personDB["12345"]
    if ok {
        fmt.Println("Found Person", person.Name, "with id 12345")
    } else {
        fmt.Println("Did not found person with id 12345")
    }
}