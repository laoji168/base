package main

import (
    "encoding/json"
    "fmt"
    "io"
    "time"
)

type Invoice struct {
    Id int
    CustomerId int
    Raised time.Time
    Due time.Time
    Paid bool
    Note string
    Items [] * Item
}

type Item struct {
    Id string
    Price float64
    Quantity int
    Note string
}

type JSONInvoice struct {
    Id int
    CustomerId int
    Raised string
    Due string
    Paid bool
    Note string
    Items [] *Item
}

type InvoiceMarshaler interface {
    MarshalInvoices(writer io.Writer, invoice []*Invoice) error
}

type InvoiceUnmarshaler interface {
    UnmarshalInvoices(reader io.Reader) ([]*Invoice, error)
}

type JSONMarshaler struct {}

func (JSONMarshaler) MarshalInvoices(writer io.Writer, invoices []*Invoice) error {
    encoder := json.NewEncoder(writer)
    if err := encoder.Encode(fileType); err != nil {
        return err
    }
    if err := encoder.Encode(fileVersion); err != nil {
        return err
    }
    return encoder.Encode(invoices)
}

func (invoice Invoice) MarshalJSON() ([]byte, error) {
    jsonInvoice := JSONInvoice{
        invoice.Id,
        invoice.CustomerId,
        invoice.Raised.Format(dateFormat),
        invoice.Due.Format(dateFormat),
        invoice.Paid,
        invoice.Note,
        invoice.Items,
    }
    return json.Marshal(jsonInvoice)

}

func readInvoices(reader io.Reader, suffix string) ([]*Invoice, error) {
    var unmarshaler InvoiceUnmarshaler
    switch suffix {
    case ".gob":
        unmarshaler = GobMarshaler{}
    case ".inv":
        unmarshaler = InvMarshaler{}
    case ".jsn", ".json":
        unmarshaler = JSONMarshaler{}
    case ".txt":
        unmarshaler = TxtMarshaler{}
    case "xml":
        unmarshaler = XMLMarshaler{}
    }
    if unmarshaler != nil {
        return unmarshaler.UnmarshalInvoice(reader)
    }
    return nil, fmt.Errorf("unrecognized input suffix: %s", suffix)
}