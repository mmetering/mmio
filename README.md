# mmetering - mmio

## Install

Clone this repository into your ```mmetering_server``` installation folder and add this app to your ```INSTALLED_APPS``` 
section – either in your default file or via appending in your production settings file.

After that add a new section to your ```my.cnf``` config file specifying the address of your EX9055DM and a value 
in percent which is used in order to decide if the LED in each flat shines red or green depending on whether more or 
less current is being produced by the solar panels and the BHKW than being fed from the outside.

```
[mmio]
address = 200
supply-threshold = 70
```


