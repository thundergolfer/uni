> source: https://sirupsen.com/napkin/problem-1/

## Napkin Problem 1: Logging Cost, Oct 2019

### Problem #1: How much will the storage of logs cost for a standard, monolithic 100,000 RPS web application?

#### Hints

You can find many numbers you might need on `sirupsen/base-rates`. 
If you don’t, consider submitting a PR! I hope for that repo to grow to be the canonical source for system’s napkin math. 

Don’t overcomplicate the solution by including e.g. CDN logs, slow query logs, etc. Keep it simple.

You might want to refresh your memory on Fermi Problems. 
Remember that you need less precision than you think. 
Remember that your goal is just to get the exponent right, x in n * 10^x.

Wolframalpha is good at calculating with units, you may use that the first few times–but 
over time the goal is for you to be able to do these calculations with no aids!


### My Answer

(Originally written with pen and paper)

`100k` RPS. `60 * 60 * 24 = 3600 * 24` is seconds per day.

```
  3600
    24
______
 14400
+72000
=86000
```

86,400 seconds per day.


`86,400 * 10^6 RPS ~= 9 * 10^3 * 10^6 ~= 9 * 10^9` requests a day.

**How many log lines per request?:** `10`

**How many bytes per log line?:** 

UTF-8 Char ~= 1 byte. `1000` chars is ~= `1000` bytes or `10^3` bytes.

**How many bytes per request?:**

`10 * 10^3 = 10^4`.

**Storage cost per GB?:**

`1GB` is `$0.01 / month`. So `10^9` bytes is `$0.01 / month`.

**How many bytes per day?**

`9 * 10^9 requests/day * 10^4 bytes/request = 9 * 10^13`. 

This is roughly `10^14`.

**How many bytes per month?**

`30 * 10^14 = 3 * 10 * 10^14 = 3 * 10^15 bytes/month`.

`30 * 10^15 / 10^9 = 3 * 10^6 GB/month`.

**Compression:**

Log data is going to be compressed on disk, so reduce data volume by a factor of 10.

`3 * 10^5 GB/month`

**Cost:**

`3 * 10^5 GB/month * 10^-2 dollars/GB = 3 * 10^3 dollars/month`

_$3000 a month to store log data._
 
### Comparison to Simon's answer.

Simon also got `$3000/month`. Woo! 

The difference was he specified `10^3 bytes/request` and I said `10^4 bytes/request`
(before compression which reduces size by factor of 10). 
Maybe Simon was implicitly including compression in that `bytes/request` figure.
