# Stormless - a app-engine storm clone, invokable via http

## Hello World
Pull this code localy and run a local instance using the `run.sh` command.
once the service is up you can run a simple word couter topology by invoking: `curl http://localhost:8080/`. After runnig the calculation you can print out the responce by invoking `curl http://localhost:8080/data`

## Usage
Topology is a dictionary of function calls. these functions must return a tuple containig the key of the next function as first member, and parameters for that function as following members of the tuple. A function may also return a list of such tuples, each will be proccesed seperatly.

It looks somthing like this:
```
{
"spout": (lambda x: ("split", "how much wood would the woodchuck chuck if the wouldchuck could chuck wood")),
"split": (lambda sentence: [("count",x) for x in sentence[0].split(' ')] ),
"count": (lambda inputs: (data.update({inputs[0]:data.get(inputs[0], 0)+1}))),
}
```

The default entrypoint will always be the function marked as "spout" which should recieve None as input.

it is also possible to send additional function definitions to simplify the topology. for examle the code 
```
global incr
def incr(x):
  return x+1
```
would enable us to use the `incr` function within our topology (note the use of `global`).

All data can be stored in the global dictionary `data`. This ditionary is returned by calling the service root URL with the addition of `/data` (see Hello World).

### API 
The string representation of the payload (which consists of a tuple of the function name, and the input to that function), the topology, and the utility functions are concatenated in this order (payload, topology, utils) using the delimiter `???` (note that means you can't use '???' in your code) and encoded to base64. The resulting string should be sent as the suffix of the url like so: http://path.to.service:8080/SOME_BASE64_STRING. The resulting `data` dictionary can be seen using `curl http://path.to.service:8080/data`
