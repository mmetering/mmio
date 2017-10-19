# mmetering - mmio

## Install

Add a new section to your ```my.cnf``` config file specifying the address of your EX9055DM and a value in percent which is used in 
order to decide if the LED in each flat lights red or green depending on wether more or less current is being produced by the 
solar panels than fed from the outside.

```
[controlboard]
address = 200
supply-threshold = 70
```


