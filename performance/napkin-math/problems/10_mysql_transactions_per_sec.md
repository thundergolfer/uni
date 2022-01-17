> https://sirupsen.com/napkin/problem-10-mysql-transactions-per-second

## Problem 10. MySQL transactions per second vs fsyncs per second

For this problem's blog post Simon gave the answers out straight away,
so I just got hands-on with his post content to learn it better.

The post uses `bpftrace`, which I couldn't get to successfully run on Codespaces.
I think I couldn't because my image's kernel version was, 5.4.something. Too high.

I could get it running using a Vagrant VM ("hashicorp/bionic64"): 

```bash
sudo snap install --devmode bpftrace
sudo apt install linux-headers-4.15.0-58-generic
```

That installs `bpftrace` so you can get the 'hello world' example working:

```
bpftrace -e 'BEGIN { printf("Hello, World!\n"); }'
```

I also needed to install these into my VM: 

```
sudo apt install cargo
sudo apt install pkg-config
```

So I could run the napkin-math program as shown in the parent dir's `readme.md`.

I need to install `mysql`

```
sudo apt install gnupg
```

and follow instructions at https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/. It's a bit tedious.

Once `mysql` is running, check which port its listening on by running `sudo mysql` and then:

```
SHOW GLOBAL VARIABLES LIKE 'PORT';
```

I got 3306.

Finally, create the `napkin` DB in `mysql`.

### Running the traces

Once the basic Rust program can connect to the `napkin` DB, start running the bpftrace
scripts Simon puts in the post.

I had to do _a lot_ of futzing around to get things working. For one, `comm == 'mysqld'` didn't
work for me, but that's what's shown in the blog posts.

I could sorta reproduce the number of fsyncs per-file by adapting Simon's script to look at `pid`.
I found the `pid` of `msql` and passed that as argument. 

My output was: 

```
Attaching 3 probes...
fd 10 -> /var/lib/mysql/ib_logfile1
fd 25 -> /var/lib/mysql/binlog.000007
fd 39 -> /var/lib/mysql/napkin/products.ibd
fd 11 -> /var/lib/mysql/#ib_16384_0.dblwr
fd 17 -> /var/lib/mysql/mysql.ibd
fd 15 -> /var/lib/mysql/undo_002
fd 13 -> /var/lib/mysql/undo_001
fd 9 -> /var/lib/mysql/ibdata1
fd 5 -> /var/lib/mysql/ib_logfile0
^C


@fsyncs[9]: 5
@fsyncs[17]: 26
@fsyncs[39]: 104
@fsyncs[13]: 202
@fsyncs[15]: 213
@fsyncs[11]: 253
@fsyncs[5]: 3149
@fsyncs[10]: 3861
@fsyncs[25]: 5269
```

This looks like Simon's output, but I have more writes to the binlog than WAL, and he had the reverse.

One thing I noticed and checked that's **really weird** is that in my VM writing the 16000 rows took 

```
Debug: 32.546902221s
Millis: 32546 ms
```

32 seconds?! That's ~10x longer than Simon says it took. What the hell is going on there.
