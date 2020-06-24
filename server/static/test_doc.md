### Testing, 123, Testing

**Source:** https://www.cipsum.com/. Leverage agile frameworks to provide a robust synopsis for high level overviews. Iterative approaches to corporate strategy foster collaborative thinking to further the overall value proposition. Organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.

Bring to the table win-win survival strategies to ensure proactive domination. At the end of the day, going forward, a new normal that has evolved from generation X is on the runway heading towards a streamlined cloud solution. User generated content in real-time will have multiple touchpoints for offshoring.

Capitalize on low hanging fruit to identify a ballpark value added activity to beta test. Override the digital divide with additional clickthroughs from DevOps. Nanotechnology immersion along the information highway will close the loop on focusing solely on the bottom line.

#### Test some credit card numbers for validity: 

```golang
package main
 
import (
    "fmt"
    "strings"
)
 
const input = `49927398716
49927398717
1234567812345678
1234567812345670`
 
var t = [...]int{0, 2, 4, 6, 8, 1, 3, 5, 7, 9}
 
func luhn(s string) bool {
    odd := len(s) & 1
    var sum int
    for i, c := range s {
        if c < '0' || c > '9' {
            return false
        }
        if i&1 == odd {
            sum += t[c-'0']
        } else {
            sum += int(c - '0')
        }
    }
    return sum%10 == 0
}
 
func main() {
    for _, s := range strings.Split(input, "\n") {
        fmt.Println(s, luhn(s))
    }
}
```

**Output:**

```
49927398716 true
49927398717 false
1234567812345678 false
1234567812345670 true
```

### Fin

Do not go gentle into that good night.
