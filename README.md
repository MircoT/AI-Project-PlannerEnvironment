AI-Project-PlannerEnvironment
=============================

An environment to test a planner agent, created for a college project and based on a problem from "Artificial Intelligence: A Modern Approach" by Stuart Russell and Peter Norvig.

## Dependencies

All you need is python. This module is tested on python 2.7.5 and 3.3.2.

## Run the application

You can create your Agent in the *agents_dir*, like MyAgent example. The name of the file must be the same
of the class that you create. The class must *inherit from LogAgent* and you have to implement the
method *solve*.

You can put your configuration file in *cfg_dir*. These files must be with json extension and they must respect
the sintax of the environment, like in the examples that you can see in this directory.

To run the application simply execute the main.py file:

```bash
python main.py [-c cfg_list] [-a agents_list]
```

**NOTE**:
* cfg_list is a list of configuration files names.
* agents_list is a list of agents names.  

*Example*: 
```bash
python main.py -c testconfig_simple.json testconfig.json -a MyAgent
```

## Contributing

Contributions are welcome, so please feel free to fix bugs, improve things, provide documentation. 
For anything submit a personal message or fork the project to make a pull request and so on... thanks!

## Notes

This library is under heavily development, so there may be substantial changes in the near future.  

You can find an example of utilization of the module in this repo. Detailed instruction will be written soon.

## License

The MIT License (MIT)

Copyright (c) 2014 Mirco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
