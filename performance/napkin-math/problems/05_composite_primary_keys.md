> https://sirupsen.com/napkin/problem-5

## Composite Primary Keys

In databases, typically data is ordered on disk by some key.
In relational databases (and definitely MySQL), as an example,
the data is ordered by the primary key of the table. For many schemas, 
this might be the `AUTO_INCREMENT` id column. A good primary key is one
that stores together records that are accessed together.

We have a `products` table with the `id` as the primary key, we might do a 
query like this to fetch 100 products for the API:

```sql
SELECT *
FROM products 
WHERE shop_id = 13 
LIMIT 100;
```

This is going to zig-zag through the product table pages on disk to load the 100 products. 
In each page, unfortunately, there are other records from other shops (see illustration below). 
They would never be relevant to `shop_id = 13`. If we are really unlucky, there may be only 1 
product per page / disk read! Each page, we'll assume, is 16 KiB (the default in e.g. MySQL). 
In the worst case, we could load 100 * 16 KiB!

(1) What is the performance of the query in the worst-case, where we load only one product per page?

(2) What is the worst-case performance of the query when the pages are all in memory cache (typically that would happen after (1))?

(3) If we changed the primary key to be `(shop_id, id)`, what would the performance be when (3a) going to disk, and (3b) hitting cache?

I love seeing your answers, so don't hesitate to email me those back!

### My Answer

(1) This isn't really 'worst case', because I think that would involve reading pages with
_zero_ matches. The query executor can't tell if a page has a match in advance. But anyway...

For worst case we'd get no page cache hits. So all 100 pages come from disk.

SSD read (random) of `8KiB` is `~100μs`. Because we're reading `16KiB`, I'll double the time,
but this may be wrong, as a random read will read an OS page at a time, and this may be `16KiB` worth anyway,
or the multiple OS pages that form the DB page will be stored sequentially in RAM. I dunno exactly.

So `200μs`.

`200μs per page * 100 pages = 20,000μs = 20ms`.

(2) Assuming page cache hits on all 100 pages, this becomes about fetching from RAM.

I chose random RAM seek performance, but wondered if sequential was more appropriate seeing
as we're fetching `16KiB` at a time. (Simon chose sequential).

Random `8KiB` RAM read is, naively, `8KiB/64 Bytes * 50ns`.

`8*2^10/64 = 8*2^10/2^6 = 2^13/2^6 = 2^7 = 128`

`128 * 50ns = 6.4μs` for one `8KiB` page. Double for `16KiB`.

`12.8μs * 100 = 1280μs ~= 1.2ms`

(3) With composite key all 100 records may fit on one page. 

If record is `<= ~16KiB / 100 = 0.16KiB` they will.

That's around `~163 bytes`. ID field is 8 bytes and so is `shop_id`, so 16 bytes from those.
`~147B` for the rest isn't a lot, but let's say it's enough to simplify.

(3a) going to disk for 1 page is then ~= 200μs

(3b) going to RAM for 1 page is then ~= 10μs.


### Comparison to Simon's answer

> https://sirupsen.com/napkin/problem-6

Simon didn't double the random disk seek time because of need to fetch 16KiB not 8KiB. This seems reasonable.
He gave the answer: `10ms`.

Simon "[assumed] sequential memory read performance for the 16Kb page", where I chose random read performance.
This seems reasonable because random RAM read performance is more relevant when you're fetching many small amounts of data,
say 8 bytes, in random locations. This is one block of `16KiB` at a time.

Interestingly, Simon notes:

> This is certainly an upper-bound, since we likely won't have the traverse the whole page in memory.

This sounds right. You just have to look at the `shop_id` portion of a record ID to select a record's byte range.

So for 3b I was off by an order of magnitude, and 3a off by a factor of 2. Not bad.
