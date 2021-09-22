## Self-driving Toy Cars

I have a _Donkey Car S1_, bought from [www.robocarstore.com](https://www.robocarstore.com/) in September 2021. 

**Community docs:** https://docs.donkeycar.com/

### Install code

This is _not_ using the monorepo's Bazel build system at the moment. The `donkeycar` library
doesn't distribute a wheel, and I'm wary of installing it from source.

```bash
cd "$(git rev-parse --show-toplevel)/machine_learning/applications/self_driving_toy_car"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Development

```
cd "$(git rev-parse --show-toplevel)/machine_learning/applications/self_driving_toy_car"
source .venv/bin/activate
```

#### Logging onto the Donker Car

TODO - You must be able to get onto the car via SSH. 


### Useful documentation

- [Donkey Car S1, Getting Started Guide](https://courses.10botics.com/path-player?courseid=donkey-car-s1-getting-started-guide&unit=donkey-car-s1-getting-started-guide_1624534699068_1Unit)
- [docs.donkeycar.com/](https://docs.donkeycar.com/)
