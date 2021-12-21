> > source: https://sirupsen.com/napkin/problem-4/

## Redis Throughput

### Napkin Problem 4

Today, as you were preparing you organic, high-mountain Taiwanese oolong in the kitchennette, 
one of your lovely co-workers mentioned that they were looking at adding more Redises because 
it was maxing out at 10,000 commands per second which they were trending aggressively towards. 
You asked them how they were using it (were they running some obscure O(n) command?). 
They'd BPF-probes to determine that it was all `GET <key>` and `SET <key> <value>`. 
They also confirmed all the values were about or less than 64 bytes. For those unfamiliar with Redis, 
it's a single-threaded in-memory key-value store written in C.

Unphased after this encounter, you walk to the window. 
You look out and sip your high-mountain Taiwanese oolong. 
As you stare at yet another condominium building being built—it hits you. 
10,000 commands per second. 10,000. Isn't that abysmally low? Shouldn't something that's fundamentally 
'just' doing random memory reads and writes over an established TCP session be able to do more?

What kind of throughput might we be able to expect for a single-thread, as an absolute upper-bound 
if we disregard I/O? What if we include I/O (and assume it's blocking each command), so it's akin 
to a simple TCP server? Based on that result, would you say that they have more investigation to 
do before adding more servers?

### My Answer

Not sure what "disregard I/O" means, but seeing the throughput of just reading from memory.

Random reads from memory are about `1 GiB / sec`. 

`64 Bytes = 2^6 bytes`. `1KiB` is `2^10`, so each value is `2^10 / 2^6 = 1/(2^4) = 1/16th` of `1KiB`.

`1KiB` is _roughly_ `1/10^6` of `1GiB`, so at `1GiB / sec` we can process roughly `16 * 10^6` values a second.

16 million is way, way bigger than 10,000. So that's my stab at disregarding I/O.

TCP network overhead is about `~10us`, which is `10^-5` fraction of a second. So you can do `10^5 = 100,000` a second.
Memory R/W is lightning fast compared to this, so request/sec is dominated by network overhead.

Roughly `100k` per second is 10x what was reported by the engineer, so something is up.  

### Comparison to Simon's answer

Basically the same answer, though he doesn't mention this "disregard I/O" explicitly again, so I don't quite get that bit.
