# Operation WIRE STORM

## Specification

We have crafted a custom protocol for broadcasting critical information between clients and servers called the CoreTech Message Protocol (CTMP).

Your mission is to write a forwarding/proxy server for the CoreTech Message Protocol (CTMP) over TCP.
The server can be written in a native language of your choice from the following:
* C
* C++
* Rust

Due to the sensitivity of this protocol, the solution should not use third-party libraries other than the chosen language’s standard library.

### CoreTech Message Protocol

```
    0               1               2               3
    0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | MAGIC 0xCC    | PADDING       | LENGTH                      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | PADDING                                                     |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | DATA ...................................................... |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
```

Each field is detailed with the following:
* MAGIC: 8 bits 0xCC.
* PADDING: 8 bits - 0x00.
* LENGTH: 16 bits - unsigned - network byte order - data size excluding the header itself.
* DATA: remaining data to be transmitted.

### Server

The server must:

* Allow a single source client to connect on port 33333.
* Allow multiple destination clients to connect on port 44444.
* Accept CTMP messages from the source and forward to all destination clients. These should be forwarded in the order they are received.
* Validate the magic and length of the data before forwarding. Any messages with an excessive length must be dropped.

### Further Information

When assessing submissions we will be looking for solutions that are, in no particular order:
* readable
* documented
* efficient

## Tests

To allow for local testing of solutions, our operatives have deployed some Python 3.12 tests for validation.

These can be run without any additional libraries:

```bash
python3 tests.py
```

The tests will output a success message if all pass, or an error message otherwise.

Good luck!
