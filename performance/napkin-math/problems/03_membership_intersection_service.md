> > source: https://sirupsen.com/napkin/problem-3/

## Membership Intersection Service

### Napkin Problem 3

You are considering how you might implement a set-membership service. 
Your use-case is to build a service to filter products by particular attributes, 
e.g. efficiently among all products for a merchant get shoes that are: black, 
size 10, and brand X.

Before getting fancy, you'd like to examine whether the simplest possible algorithm 
would be sufficiently fast: store, for each attribute, a list of all product ids for 
that attribute (see drawing below). Each query to your service will take the form: 
`shoe AND black AND size-10 AND brand-x`. To serve the query, you find the intersection 
(i.e. product ids that match in all terms) between all the attributes. This should return 
the product ids for all products that match that condition. In the case of the drawing below, 
only P3 (of those visible) matches those conditions.

The largest merchants have 1,000,000 different products. Each product will be represented in this 
naive data-structure as a 64-bit integer. 
While simply shown as a list here, you can assume that we can perform the intersections 
between rows efficiently in O(n) operations. In other words, in the worst case you have to 
read all the integers for each attribute only once per term in the query. We could implement 
this in a variety of ways, but the point of the back-of-the-envelope calculation is to not 
get lost in the weeds of implementation too early.

What would you estimate the worst-case performance of an average query with 4 AND conditions to be? Based on this result and your own intuition, would you say this algorithm is sufficient or would you investigate something more sophisticated?
    
### My Answer

I initially got a bit hung up on how the intersection between rows
would be `O(n)`. I wrote some pseudocode, which didn't reveal much, then
decided just to accept that the set intersection function would be dominated by
the time to read all the 64 bit ints.

Taking the biggest customer as the worst cases, we have `10^6 * 64bit = 8MB` for each attribute.
Doing 4 `AND` intersection operations makes `32MB` of data.

It will matter whether the data is on disk or in-memory when it comes time to process,
so let's work that out:

* `10^3` attrs -> `8000MB = 8GB` of data (in-memory feasible)
* `10^6` attrs -> `8000GB = 8TB` of data (in-memory *not* feasible)
* `10^4` attrs -> `80GB` of data (in-memory feasible)

Max 10,000 attributes seems reasonable, and certainly 1,000. But some crazy merchants
may need up-to a million attributes so lets check that as well.

_NOTE:_ At this point I didn't fully realize that we need to think of the memory requirements as being
per-merchant. You can shard your customers, obviously, but storing 80GB in-memory for multiple customers
is quite an ask.

#### Memory

Read `1MiB` from memory, sequentially: `100 - 250μs`. On 2021 computers, it's `~100μs`.

`100μs * 8MB per attr ~= 800μs` (approx not exact because `8MB != 8MiB`).

`800 * 4 = 3,200μs = 3.2ms` overall.

This is definitely fast enough for a request. This is supposed to be _worst case_, 
and a reasonable request budget may go up to 100ms.

(I didn't think about $$ costs, but Simon did)   

#### Disk

Read `1MiB` from SSD: `~= 250μs` (napkin math repo says `~200μs`)

`250μs * 8 = 2ms per attr`

`2ms * 4 attr = 8ms`.

This is also fast enough. (Damn, modern SSDs are _fast_)

An LRU cache of attribute listings would make average processing time
much closer to an 'in-memory only' implementation.  


### Comparison to Simon's answer

Simon mentions $$$.

> That'd cost us about $8 in memory, or about $1 to store on disk.

That must be per-month. Good idea to mention $$$ when you're talking about
feature cost that scales with customer acquisition.

I disagree with Simon saying SSD-based processing would take 320ms. 

> For SSD (about 10x cheaper, and 10x slower than memory), 320 ms. 300 ms is way too high, but 3 ms is acceptable. 

That's 100x worse than RAM, which seems contradicted by the numbers he has in his `napkin-math` repo. 
I've DM'd him on Twitter to follow-up (_Update:_ Simon replied on Twitter and has now updated the post 👍).
