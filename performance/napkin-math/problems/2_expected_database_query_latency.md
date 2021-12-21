> source: https://sirupsen.com/napkin/problem-2/

### Problem #2: Your SSD-backed database has a usage-pattern that rewards you with a 80% page-cache hit-rate... 

(i.e. 80% of disk reads are served directly out of memory instead of going to the SSD). 
The median is 50 distinct disk pages for a query to gather its query results (e.g. InnoDB pages in MySQL). 
What is the expected average query time from your database?

### My Answer

I made the **big mistake** of thinking the 80% caching was on the whole query, not per-page.
This mis-structured my entire answer, though I got pretty close to correct in the end, luckily.

##### Ave. query time from RAM

`50` pages at `64KiB / page` = `3200 KiB = 3.2 MiB Query`.

This has an _incorrect_ guess that a DB page is `64 KiB`. They're typically `8KiB`,
so my answer was overweight by a factor of 8.

`1MiB` from RAM is roughly `250` microseconds, if read sequentially.
In RAM the pages wouldn't be sequential, so this was wrong, but I only realised that
later in my working.

`3.2 x 250 micro` is `800 micro` for RAM read.

I add ~200 micro for the DB overhead, which includes query plan compiling
and network to round up to `~1ms` for the response. This estimate for DB overhead
is likely an underestimate.

##### Ave. query time from SSD disk

Random SSD seek for `8KiB` is `100 microsecs`.

`8 * 50 pages * 100µs = 400 * 100µs = 40,000µs = 40ms`

So roughly `40ms` for the SSD-based query. Here I assume that DB overhead is negligible
relative to the time to retrieve data from disk.

_Remember that I was fundamentally wrong to miss that the caching was per-page,
not per query._ I got a hint of this when I wondered how a DBMS would have an entire
query plan, but it didn't click.

##### Averaging

`0.8 * 1ms + 0.2 * 40ms ~= 9ms` average query time.

Simon says "Somewhere between 1-10ms seems reasonable", so remarkably I've
gotten the 'right' answer despite being mostly wrong in my thinking.

### Comparison to Simon's answer

Simon didn't make the mistake of doing per-query caching. Like the question
poses, it's per-page caching. The DBMS _buffer manager_ will be keeping pages in
memory, and there's an 80% page-cache hit rate for that.

`50 * 0.8 = 40` RAM page reads. 10 SSD reads.

10 SSD reads require random disk seek of `8KiB` (as DB page is typically 8 not 64 KiB like I said).

A random read of `8KiB` from SSD is roughly `100µs`, so `1ms` lower bound on the non-cached pages.

How much is the 40 RAM-based page reads? Reading `64B` from RAM randomly is roughly `5 nanosecs`.

A `8KiB` page is roughly `8000/64 ~= 120x` the size of `64B`, so guesstimate `5 * 120 = 600 nanosecs`
to read a page. So less than a microsecond.

Simon just said: 

> The page-cache reads will all be less than a microsecond, so we won't even factor them in.
> It's typically the case that we can ignore any memory latency as soon as I/O is involved.

But I've gone into a bit more detail to confirm.

`40 * 600 nanoseconds = 24000 nanoseconds = 24µs` to read the cached pages.

`1000µs` for disk-based pages + `24µs` for RAM-based pages = `~1024µs` lower bound on average query time.

Simon concludes:

> Somewhere between 1-10ms seems reasonable, when you add in database-overhead
> and that 1ms for disk-access is a lower-bound.
