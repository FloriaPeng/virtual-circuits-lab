# virtual-circuits-lab
The **backend** of the web-based virtual circuits lab.  
It is built using `Python` with `Flask`.  
Please refer to our **frontend** at [circuit-simulator-frontend](https://github.com/YukaiZhang2019/circuit-simulator-frontend).

## To Install Required Packages
#### For PySpice Only
1. PyCharm:  
    *settings -> project -> Python Interpreter:*  
        *install:* `PySpice`
2. Run the following on command line:
```
pyspice-post-installation --install-ngspice-dll
pyspice-post-installation --check-install
```

## To Run
Run `app.py`.  
For other steps, please refer to the instructions in our [frontend repository](https://github.com/YukaiZhang2019/circuit-simulator-frontend).

## To Test
Use [Postman](https://www.postman.com/) to send HTTP Requests and receive HTTP Responses.

## PySpice Documentation
Please refer to [PySpice](https://github.com/FabriceSalvaire/PySpice).
