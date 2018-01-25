# Stormless - a app-engine storm clone, invokable via http

## Hello World
Pull this code localy and run a local instance using the `run.sh` command.
once the service is up you can run a simple word couter topology by invoking: `curl http://localhost:8080/`. After runnig the calculation you can print out the responce by invoking `curl http://localhost:8080/data`

## Usage
Topology is a dictionary of function calls. these functions must return a tuple containig the key of the next function as first member, and parameters for that function as following members of the tuple. A function may also return a list of such tuples, each will be proccesed seperatly.

It looks somthing like this:
```
{
\"spout\": (lambda x: (\"split\", \"how much wood would the woodchuck chuck if the wouldchuck could chuck wood\")),
\"split\": (lambda sentence: [(b\"count\",x) for x in sentence[0].split(\' \')] ),
\"count\": (lambda inputs: (data.update({inputs[0]:data.get(inputs[0], 0)+1}))),
}
```

The entrypoint will always be the function marked as "spout" which should recieve None as input.

it is also possible to send additional function definitions to simplify the topology. for examle the code 
```
global incr
def incr(x):
  return x+1
```
would enable us to use the `incr` function within our topology.

All data can be stored in the global dictionary `data`. This ditionary is returned by calling the service root URL with the addition of `/data` (see Hello World)
   
