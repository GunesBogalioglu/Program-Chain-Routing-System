# Python based Program Chain Routing System (WIP)
This project uses python to chain link defined apps to optimize, compress or whatever user wants to do with their files.
### Usage:
 - Move your tool to the tools folder.
 - Create a json file for your tool like [example](https://github.com/GunesBogalioglu/Program-Chain-Routing-System/blob/main/tools/method.example)
 - Move your files to the input folder **(always backup your files)**
 - Change concurrent_worker_count and other settings as you like. (Yeah I know I should keep them in settings file)
 - Run
 
 # Example Usage
### - Photo optimization

pingo->jpeg-recompress->mozjpegtran

|File Name|Method|Original Size|Compressed Size|
|---------|------|-------------|---------------|
|dictionary.jpg|Lossless|3,23 MB|2,96 MB|
|dictionary.jpg|Lossy|3,23 MB|1,16 MB|

### Disclaimer:
This project is a personal hobby project and may be updated or modified as desired. Please note that this project is not considered to be complete and may not be suitable for use in a production environment.
